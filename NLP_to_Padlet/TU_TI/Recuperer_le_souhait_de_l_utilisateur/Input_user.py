
##########################   TU : Récupérer le souhait de l'utilisateur   ###########################
#   Exigences :                                                                                     #
#   Si l'utilisateur saisit un texte de moins de 10 caractères alors on n'accepte pas sa demande    #
#   Si la saisit n'est pas sous format texte (un nombre par exemple) on n'accepte pas la demande    #
#####################################################################################################

def check_invalid_input(user_input):
    total_characters = len(user_input)
    if total_characters < 10:
        return True  # Le texte doit contenir au moins 10 caractères

    # Compter le nombre de chiffres et de ponctuations
    count_digits_punctuation = sum(char.isdigit() or char in ",?;.:/!§%*^¨$£&'{()}-|`_\\@][=" for char in user_input)
    #print(count_digits_punctuation)

    # Vérifier si plus de 50% de la chaîne est composée de chiffres ou de ponctuations
    if count_digits_punctuation > total_characters / 2:
        return True  # Plus de 50% de chiffres ou de ponctuations, donc invalide

    return False  # La saisie est valide

# Demander à l'utilisateur de saisir un texte jusqu'à ce qu'il fournisse une saisie valide
def saisi_input():
    while True:
        user_input = input("Saisissez un texte (au moins 10 caractères) : ")

        if check_invalid_input(user_input):
            print("La saisie n'est pas valide. Réessayez.")
        else:
            break

    print("Vous avez saisi un texte valide.")
    return user_input