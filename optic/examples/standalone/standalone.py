import optic as op

print("op.text", dir(op))


@op.page()
def main():
  op.text(text="123")


# TODO: un-comment this once I figured out the CLI/execution story more.
# if __name__ == "__main__":
#   op.run()
