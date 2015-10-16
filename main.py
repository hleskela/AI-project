from reinforcement_learning_class import reinforcement_learing

answer = raw_input("Do you need to generate training files (Y/N): ")

if answer in ['Y', 'y', 'N', 'n']:
    if answer == 'Y' or answer == 'y':
        from files_generator import files_generator
        generat_file = files_generator()
        generat_file.generator()

    test = reinforcement_learing()
    print("\nGood! Time to start training!\n")
    num_of_words = input("Enter the start for number of words to check: ")
    end = input("Enter the end point : ")
    steps = input("Enter the step: ")

    print(test.brute_force_rl(num_of_words, end, steps))
else:
    print("Please enter 'Y' or 'N'")
