#!/usr/bin/env python3

from captacity import add_captions
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Caption a video file.")
    parser.add_argument("video_file", help="Path to the input video file.")
    parser.add_argument("output_file", help="Path to the output video file.")
    parser.add_argument("--max_words_per_frame", type=int, default=5, help="Maximum words displayed per frame.")
    
    args = parser.parse_args()

    if not os.path.exists(args.video_file):
        print(f"Error: The video file '{args.video_file}' does not exist.")
        return

    add_captions(
        video_file=args.video_file,
        output_file=args.output_file,
        print_info=True,
        max_words_per_frame=args.max_words_per_frame
    )

if __name__ == "__main__":
    main()
