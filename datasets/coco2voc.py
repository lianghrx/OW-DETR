import xml.etree.cElementTree as ET
import os

from pycocotools.coco import COCO


def imagesets(coco_annotation_file, target_folder):
    # os.makedirs(os.path.join(target_folder, 'Main'), exist_ok=True)
    # import pdb;pdb.set_trace()
    coco_instance = COCO(coco_annotation_file)
    with open("data/VOC2007/ImageSets/Main/train.txt", "a") as myfile:
        for index, image_id in enumerate(coco_instance.imgToAnns):
            image_details = coco_instance.imgs[image_id]
            myfile.write(image_details['file_name'].split('.')[0])
            myfile.write('\n')


def coco_to_voc_detection(coco_annotation_file, target_folder):
    os.makedirs(os.path.join(target_folder, 'Annotations'), exist_ok=True)
    coco_instance = COCO(coco_annotation_file)
    for index, image_id in enumerate(coco_instance.imgToAnns):
        # import pdb;pdb.set_trace()
        image_details = coco_instance.imgs[image_id]
        annotation_el = ET.Element('annotation')
        ET.SubElement(annotation_el, 'filename').text = image_details['file_name']

        size_el = ET.SubElement(annotation_el, 'size')
        ET.SubElement(size_el, 'width').text = str(image_details['width'])
        ET.SubElement(size_el, 'height').text = str(image_details['height'])
        ET.SubElement(size_el, 'depth').text = str(3)

        for annotation in coco_instance.imgToAnns[image_id]:
            object_el = ET.SubElement(annotation_el, 'object')
            # import pdb;pdb.set_trace()
            ET.SubElement(object_el,'name').text = coco_instance.cats[annotation['category_id']]['name']
            # ET.SubElement(object_el, 'name').text = 'unknown'
            ET.SubElement(object_el, 'difficult').text = '0'
            bb_el = ET.SubElement(object_el, 'bndbox')
            ET.SubElement(bb_el, 'xmin').text = str(int(annotation['bbox'][0] + 1.0))
            ET.SubElement(bb_el, 'ymin').text = str(int(annotation['bbox'][1] + 1.0))
            ET.SubElement(bb_el, 'xmax').text = str(int(annotation['bbox'][0] + annotation['bbox'][2] + 1.0))
            ET.SubElement(bb_el, 'ymax').text = str(int(annotation['bbox'][1] + annotation['bbox'][3] + 1.0))

        ET.ElementTree(annotation_el).write(os.path.join(target_folder, 'Annotations', image_details['file_name'].split('.')[0] + '.xml'))
        if index % 10000 == 0:
            print('Processed ' + str(index) + ' images.')


if __name__ == '__main__':
    files = ['instances_train2017.json', 'instances_val2017.json']
    coco_annotation_path = 'data/coco/annotations'
    target_folder = 'data/OWDETR/VOC2007'
    for filename in files:
        filepath = os.path.join(coco_annotation_path, filename)
        coco_to_voc_detection(filepath, target_folder)
        # imagesets(filepath, target_folder)