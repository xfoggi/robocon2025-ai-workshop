#!/usr/bin/env python3
"""
MarkdownResultListener.py

A Robot Framework listener that creates a markdown file (result.md)
with a table of executed tests and their status.
"""

class MarkdownResultListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        # Initialize an empty list to store test results.
        self.results = []
        print("MarkdownResultListener started.")

    def start_test(self, data, result):
        # Optionally log or perform actions at test start.
        pass

    def end_test(self, data, result):
        # Called when a test ends.
        # Append a tuple with the test name and its status.
        self.results.append((data.name, result.status))
        print(f"Test ended: {data.name} - {result.status}")

    def close(self):
        # Called when the entire test run is complete.
        # Write the collected test results into a markdown file as a table.
        try:
            with open("result.md", "w", encoding="utf-8") as f:
                f.write("# Test Execution Results\n\n")
                f.write("| Test Name | Status |\n")
                f.write("|-----------|--------|\n")
                for name, status in self.results:
                    f.write(f"| {name} | {status} |\n")
            print("Results written to result.md")
        except Exception as e:
            print(f"Error writing result.md: {e}")