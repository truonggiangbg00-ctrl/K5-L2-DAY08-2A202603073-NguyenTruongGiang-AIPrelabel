"""Run the deployed local YOLOE Nuclio function through the lab COCO pipeline.

The function has fixed prompts and imgsz=640. Polygon extents supply its boxes.
This avoids the Windows regex DLL blocked by Application Control; inference
runs in the user's existing Linux CVAT model container.
"""
import argparse
import base64
import json
import sys
import urllib.request
from urllib.parse import urlparse

import prelabel


class LocalYoloE(prelabel.Backend):
    needs_prompts = True
    native_masks = True
    endpoint = ''

    def detect(self, path):
        payload = json.dumps({'image': base64.b64encode(path.read_bytes()).decode(),
                              'threshold': self.min_conf}).encode()
        request = urllib.request.Request(self.endpoint, data=payload,
                                         headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=180) as response:
            predictions = json.load(response)
        output = []
        for prediction in predictions:
            if prediction['label'] != 'three_wheeler':
                continue
            points = prediction['points']
            polygons = None
            if prediction['type'] == 'polygon':
                xs, ys = points[::2], points[1::2]
                box = (min(xs), min(ys), max(xs), max(ys))
                if self.a.segmenter == 'native':
                    polygons = [points]
            else:
                box = tuple(points)
            output.append(('tuk tuk three wheeler', float(prediction['confidence']), box, polygons))
        return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--endpoint', required=True)
    args, rest = parser.parse_known_args()
    if urlparse(args.endpoint).hostname not in ('localhost', '127.0.0.1'):
        parser.error('Only the local CVAT model endpoint is supported.')
    LocalYoloE.endpoint = args.endpoint
    prelabel.BACKENDS['yoloe'] = LocalYoloE
    sys.argv = [sys.argv[0]] + rest + ['--model', 'yoloe', '--size', 's', '--device', 'cpu',
        '--classes', 'three_wheeler', '--imgsz', '640',
        '--prompts', 'tuk tuk three wheeler=three_wheeler',
        '--note', 'Live local Nuclio YOLOE-26s; fixed 7-class prompts; polygon extent boxes; imgsz=640; AI-assisted execution']
    prelabel.main()
