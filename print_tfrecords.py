"""
function:读取打印tfrecords
"""


import tensorflow as tf
import os

def print_tf(input_filename):
    print("Try to print the tfrecords file: {}".format(input_filename))

    max_print_number = 10
    current_print_index = 0

    for serialized_example in tf.python_io.tf_record_iterator(input_filename):
        # Get serialized example from file
        example = tf.train.Example()
        example.ParseFromString(serialized_example)
        label = example.features.feature["label"].int64_list.value
        features = example.features.feature["features"].float_list.value
        print("Index: {}, label: {}, features: {}".format(current_print_index, label, features))

        # Return when reaching max print number
        current_print_index += 1
        if current_print_index > max_print_number - 1:
            return


def main():
  current_path = os.getcwd()
  for filename in os.listdir(current_path):
    if filename.startswith("") and filename.endswith(".tfrecords"):
      tfrecords_file_path = os.path.join(current_path, filename)
      print_tf(tfrecords_file_path)


if __name__ == "__main__":
  main()