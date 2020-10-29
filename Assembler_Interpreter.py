import re
def assembler_interpreter(program):
    program = re.sub(' +', ' ', program).splitlines()
    regs = dict()
    i = 0
    get_value = lambda v: regs[v] if v in regs else int(v)
    cmp_res = None
    labels = dict()
    ret_pointers = list()
    output = ""
    for i in range(len(program)):
        cmd = program[i].split(" ")
        if cmd[0].endswith(":"):
            labels[cmd[0][:-1]] = i
    i = 0
    while i < (len(program)):
        program[i] = program[i].lstrip()
        cmd = program[i].split(" ")
        if cmd[0] == 'end':
            return output
        elif cmd[0] == 'msg':
            cmd = re.findall(r"[\w']+", program[i])
            cmd2 = program[i].split("'")
            j = 1
            k = 0
            while k < len(cmd):
                if cmd[k] in regs:
                    output += str(regs[cmd[k]])
                elif cmd[k][0] == "'":
                    if j < len(cmd2):
                        output += str(cmd2[j])
                        j += 2
                        k += 1
                k += 1
        elif cmd[0] == 'ret':
            i = ret_pointers.pop()
            continue
        elif cmd[0] == 'call':
            ret_pointers.append(i+1)
            i = labels[cmd[1]]
            continue
        elif cmd[0] == 'cmp':
            cmp_res = float(regs[cmd[1][0]] + 1) / (get_value(cmd[2]) + 1)
        elif not cmd or cmd[0] == ';':
            i += 1
            continue
        elif cmd[0] == 'mov':
            regs[cmd[1][:-1]] = get_value(cmd[2])
        elif cmd[0] == 'inc':
            regs[cmd[1]] += 1
        elif cmd[0] == 'dec':
            regs[cmd[1]] -= 1
        elif cmd[0] == 'jnz':
            if (cmd[1].lstrip("-").isnumeric() and cmd[1] != 0) or regs[cmd[1]] != 0:
                i += int(cmd[2])
                continue
        elif cmd[0] == 'add':
            regs[cmd[1][:-1]] += get_value(cmd[2])
        elif cmd[0] == 'sub':
            regs[cmd[1][:-1]] -= get_value(cmd[2])
        elif cmd[0] == 'mul':
            regs[cmd[1][:-1]] *= get_value(cmd[2])
        elif cmd[0] == 'div':
            regs[cmd[1][:-1]] = int(regs[cmd[1][:-1]] / get_value(cmd[2]))
        else:
            jump = False
            if cmd[0] == 'jmp': jump = True
            elif cmd[0] == 'jne' and cmp_res != 1: jump = True
            elif cmd[0] == 'je' and cmp_res == 1: jump = True
            elif cmd[0] == 'jge' and cmp_res >= 1: jump = True
            elif cmd[0] == 'jg' and cmp_res > 1: jump = True
            elif cmd[0] == 'jle' and cmp_res <= 1: jump = True
            elif cmd[0] == 'jl' and cmp_res < 1: jump = True
            if jump:
                i = labels[cmd[1]]
                continue
        i += 1
    return -1