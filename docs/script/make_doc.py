import re
import os

doc_file_path = [ 
    'esphome-docs/climate/haier.rst',
    'esphome-docs/sensor/haier.rst',
    'esphome-docs/binary_sensor/haier.rst',
    'esphome-docs/text_sensor/haier.rst',
    'esphome-docs/button/haier.rst',
    'esp32_backup.rst',
    'additional_information.rst',
]

def process_esphome_refs(line, l_num):
    esphome_refs = [
        (":ref:`uart`", "`UART Bus <https://esphome.io/components/uart#uart>`_"),
        (":ref:`config-id`", "`ID <https://esphome.io/guides/configuration-types.html#config-id>`_"),
        (":ref:`config-time`", "`Time <https://esphome.io/guides/configuration-types.html#config-time>`_"),
        (":ref:`Automation <automation>`", "`Automation <https://esphome.io/guides/automations#automation>`_"),
        (":ref:`haier-on_alarm_start`", "`on_alarm_start Trigger`_"),
        (":ref:`haier-on_alarm_end`", "`on_alarm_end Trigger`_"),
        (":ref:`Climate <config-climate>`", "`Climate <https://esphome.io/components/climate/index.html#config-climate>`_"),
        (":ref:`lambdas <config-lambda>`", "`lambdas <https://esphome.io/guides/automations#config-lambda>`_"),
        (":ref:`Sensor <config-sensor>`", "`Sensor <https://esphome.io/components/sensor/index.html#config-sensor>`_"),
        (":ref:`Binary Sensor <config-binary_sensor>`", "`Binary Sensor <https://esphome.io/components/binary_sensor/index.html#base-binary-sensor-configuration>`_"),
        (":ref:`Text Sensor <config-text_sensor>`", "`Text Sensor <https://esphome.io/components/text_sensor/index.html#base-text-sensor-configuration>`_"),
        (":ref:`Button <config-button>`", "`Text Sensor <https://esphome.io/components/button/index.html#base-button-configuration>`_"),

    ]
    res = line
    for o, r in esphome_refs:
        res = res.replace(o, r)
    if res.find(":ref:") != -1:
        print(f"\tWarning: ref found, line #{l_num}")
    return res

def process_figure(section, output_file, pth):
    m = re.match(r"^( *\.\. +figure:: +)(.+) *$", section[0])
    if m:
        new_url = "./docs/"
        if len(pth) > 0:
            new_url += pth + "/"
        new_url += m.group(2)
        width = "100"
        center = False
        desc = ""
        for sl in section[1:]:
            if not sl.strip().startswith(":"):
                if len(sl.strip()) > 0:
                    desc += f"<br><i>&emsp;{sl.strip()}</i>"
            if re.match(r"^   *:align: +center *$", sl):
                center = True
            else:
                m = re.match(r"^   *:width: +(\d+)(?:\.\d+)?\%$", sl)
                if m:
                    width = m.group(1)
        htm = f"<img src=\"{new_url}?raw=true\" height=\"{width}%\" width=\"{width}%\">"
        output_file.write(f".. raw:: HTML\n\n  <p><a href=\"{new_url}?raw=true\">{htm}</a>{desc}</p>\n\n")

def process_section(section, output_file, pth):
    print(f"\tProcessing section: {section[0].strip()}")
    if section[0] == ".. seo::\n":
        pass
    elif section[0].startswith(".. figure::"):
        process_figure(section, output_file, pth)
    else:
        output_file.writelines(section)

document_header = [
    ".. This file is automatically generated by ./docs/script/make_doc.py Python script.\n",
    "   Please, don't change. In case you need to make corrections or changes change\n",
    "   source documentation in ./doc folder or script.\n\n"
]

output_file = open("../../README.rst", "w")
output_file.writelines(document_header)
for in_f in doc_file_path:
    print(f"Processing: {in_f}")
    output_file.write(f".. Generated from {in_f}\n\n")
    input_file = open(f"../{in_f}", "r")
    p = os.path.dirname(in_f)
    lines = input_file.readlines()
    is_seo = False
    is_section = False
    section = []
    l_counter = 0
    for line in lines:
        l_counter += 1
        if line == "See Also\n":
            break
        if is_section:
            if (line in ['\n', '\r\n']) or line.startswith("  "):
                section.append(line)
                continue
            else:
                is_section = False
                process_section(section, output_file, p)
        if (not is_section) and line.startswith(".. "):
            is_section = True
            section = [ line ]
            continue
        if line == ".. seo::\n":
            is_seo = True
            continue
        if is_seo:
            if not line.startswith("    :"):
                is_seo = False
            continue
        l = process_esphome_refs(line, l_counter)
        output_file.write(l)
    print(f"\tProcessed {l_counter} line(s)")