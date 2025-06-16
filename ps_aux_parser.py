import subprocess
from datetime import datetime


def get_ps_aux_output():
    result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()


def parse_ps_aux(ps_aux_output):
    processes = ps_aux_output[1:]

    total_cpu = 0.0
    total_mem = 0.0
    user_process_count = {}
    max_mem_proc = ("", 0.0)
    max_cpu_proc = ("", 0.0)

    for process in processes:
        line = process.split(None, 10)
        user = line[0]
        cpu = float(line[2])
        mem = float(line[3])
        cmd = line[10]

        total_cpu += cpu
        total_mem += mem

        user_process_count[user] = user_process_count.get(user, 0) + 1

        if mem > max_mem_proc[1]:
            max_mem_proc = (cmd, mem)
        if cpu > max_cpu_proc[1]:
            max_cpu_proc = (cmd, cpu)

    return {
        "users": list(user_process_count.keys()),
        "total_processes": len(ps_aux_output) - 1,
        "user_processes": user_process_count,
        "total_mem": total_mem,
        "total_cpu": total_cpu,
        "max_mem_proc": max_mem_proc,
        "max_cpu_proc": max_cpu_proc,
    }


def generate_report(data):
    lines = []
    lines.append("Отчёт о состоянии системы:")
    lines.append(f"Пользователи системы: {', '.join(data['users'])}")
    lines.append(f"Процессов запущено: {data['total_processes']}")
    lines.append("\nПользовательских процессов:")
    for user, count in data["user_processes"].items():
        lines.append(f"{user}: {count}")
    lines.append(f"\nВсего памяти используется: {data['total_mem']:.1f}%")
    lines.append(f"Всего CPU используется: {data['total_cpu']:.1f}%")
    lines.append(
        f"Больше всего памяти использует: ({data['max_mem_proc'][0][:20]}, {data['max_mem_proc'][1]:.1f}%)"
    )
    lines.append(
        f"Больше всего CPU использует: ({data['max_cpu_proc'][0][:20]}, {data['max_cpu_proc'][1]:.1f}%)"
    )

    return "\n".join(lines)


def save_report(report_text):
    now = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")
    filename = f"{now}-scan.txt"
    with open(filename, "w") as f:
        f.write(report_text)


def main():
    ps_aux_output = get_ps_aux_output()
    parsed_data = parse_ps_aux(ps_aux_output)
    report = generate_report(parsed_data)
    save_report(report)


if __name__ == "__main__":
    main()
