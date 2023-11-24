import optic as op

print("op.text", dir(op))


@op.page()
def main():
    op.text(text="123")


if __name__ == "__main__":
    op.run()
