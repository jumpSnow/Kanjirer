from Jisho.jisho import Jisho

char = "女"
test = Jisho(char)

for strokes, frequency, grade, jlpt, parts, radicals, on_readings, kun_readings, on_readings_compounds, kun_readings_compounds in test.data:
    print("strokes:", strokes)
    print("frequency: ", frequency)
    print("grade: ", grade)
    print("jlpt: ", jlpt)
    print("parts: ", parts)
    print("radicals: ", radicals)
    print("on_readings: ", on_readings)
    print("kun_readings: ", kun_readings)
    print("on_readings_compounds: ", on_readings_compounds)
    print("kun_readings_compounds: ", kun_readings_compounds)




