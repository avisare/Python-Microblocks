import psutil


def get_cpu_info():
    return psutil.cpu_times_percent(1)[0], psutil.virtual_memory()[2]


def main():
    cpu_percentage, memory_usage = get_cpu_info()
    print(f"CPU percentage is equal to: {cpu_percentage} %")
    print(f"Memory usage is equal to {memory_usage} %")


if __name__ == "__main__":
    main()
