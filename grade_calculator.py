while True:
    try:
        a_1 = int(input("Enter score for Assessment 1 between 1-100: "))
        a_2 = int(input("Enter score for Assessment 2 between 1-100: "))
        a_3 = int(input("Enter score for Assessment 3 between 1-100: "))
        a_4 = int(input("Enter score for Assessment 4 between 1-100: "))
        if (a_1 > 100) or (a_2 > 100) or (a_3 > 100) or (a_4 > 100) or (a_1 < 1) or (a_2 < 1) or (a_3 < 1) or (a_4 < 1):
            print("Input value between 1 and 100")
        else:
            break
    except ValueError:
        print("Enter valid number")

e_credits = 0
m_credits = 0
a_credits = 0
na = 0

a_1_worth = 6
a_2_worth = 6
a_3_worth = 4
a_4_worth = 3
total_credits = 19

gpa = ((a_1 * a_1_worth) + (a_2 * a_2_worth) + (a_3 * a_3_worth) + (a_4 * a_4_worth)) / total_credits


def assign_letter(assessment, worth):
    global e_credits, m_credits, a_credits, na

    if assessment > 85:
        e_credits += worth
        return "E"
    elif assessment > 65:
        m_credits += worth
        return "M"
    elif assessment > 50:
        a_credits += worth
        return "A"
    else:
        na += worth
        return "N"


grade1 = assign_letter(a_1, a_1_worth)
grade2 = assign_letter(a_2, a_2_worth)
grade3 = assign_letter(a_3, a_3_worth)
grade4 = assign_letter(a_4, a_4_worth)

endorsement = "No Endorsement"

if e_credits >= 14 and grade4 == "E":
    endorsement = "Excellence"
elif m_credits >= 14 and (grade4 == "M") or (grade4 == "E"):
    endorsement = "Merit"


print("\n----GRADE RESULTS----\n")

print(f"Assessement 1: {a_1}/100")
print(f"Assessement 2: {a_2}/100")
print(f"Assessement 3: {a_3}/100")
print(f"Assessement 4: {a_4}/100\n")

print(f"Your GPA is {gpa}")

print(f"You got {e_credits} Excellence credits")
print(f"User has {m_credits} Merit credits")
print(f"User has {a_credits} Achieved credits")
print(f"User has {na} not Achieved ")

if endorsement != "No Endorsement":
    print(f"Congratulations, you got {endorsement} endorsement")
else:
    print("You didn't get an endorsement")