import os
import gherkan.utils.constants as c

from gherkan.flask_api.raw_text_to_signal import nl_to_signal

# request = {
#     "feature": "robot R4",
#     "feature_desc": "Robot R4 je kolaborativní robot Kuka IIWA. Má za úkol finální kompletaci autíčka. Postupně mu jsou na jeho stanici XX přivezeny zkompletované součásti autíčka. Robotu je nejdříve přivezono chassi autíčka. Následuje body (korba) a jako poslední je přivezena kabina.",
#     "background": "given line is on",
#     "text_raw": "scenario   As soon as robot R1 finished sorting all cubes, shuttle goes to station XXX",
#     "language": "en"
# }

request = {
    "feature" : "Montrac",
    "feature_desc" : " Montrac je dopravníkový systém s několika samostatnými vozíčky. Tyto vozíčky přepravují částečně zkompletované výrobky mezi několika stanicemi.",
    "background" : "pokud je linka zapnutá",
    "text_raw" : "scenario pokud je linka zapnutá",
    "language" : "cs"
}

base_path = os.path.join(c.DATA_DIR, "output", "raw_out")

import cProfile

pr = cProfile.Profile()
pr.enable()
nl_to_signal(base_path, request)
pr.disable()

pr.dump_stats("/windows/Soubory/Projekty/CIIRC/nl_instruction_processing/profile_cs.prof")

nl_file_path = base_path + ".feature"
signal_file_path = base_path + "_signals.feature"

print("\n\n--- NL FILE ---")
with open(nl_file_path, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)

print("\n\n--- SIGNAL FILE ---")
with open(signal_file_path, "rt", encoding="utf-8") as f:
    text = f.read()
    print(text)