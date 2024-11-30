import random
import time
import operator

# Define players by rarity
players_by_rarity = {
    "Legendary": [
        "Lionel Messi", "Andres Iniesta", "Xavi Hernandez", "Ronaldinho", "Carles Puyol",
        "Johan Cruyff", "Samuel Eto'o", "Rivaldo", "Pep Guardiola", "Diego Maradona",
        "Dani Alves", "Deco", "Luis Suarez", "Ronald Koeman", "Sergio Busquets",
        "Romário", "Zlatan Ibrahimović", "Ronaldo Nazario", "Thierry Henry", "Neymar Jr",
    ],
    "Epic": [
        "Gerard Pique", "Marc-Andre ter Stegen", "Ronald Araujo", "Jules Kounde", "Pau Cubarsi", "Lamine Yamal",
        "Joao Cancelo", "Ivan Rakitić", "Victor Valdés", "David Villa", "Lewandowski", "Pedri",
        "Jordi Alba", "Yaya Touré", "Alexis Sánchez", "Cesc Fàbregas", "Gavi", "Frenkie de Jong", "Alejandro Balde", "Dani Olmo",
    ],
    "Rare": [
        "Ansu Fati", "Ferran Torres", "Aubameyang", "Joao Felix", "Paulinho", "Coutinho", "Christensen",
        "Raphinha", "Ousmane Dembele", "Martin Braithwaite", "Miralem Pjanic", "Samuel Umtiti", "Hector Fort",
        "Adama Traoré", "Fermin Lopez", "Sergiño Dest", "Gundogan", "Memphis Depay", "Marc Casado", "Marc Bernal",
    ],
    "Common": [
        "Eric Garcia", "Sergi Roberto", "Marcos Alonso", "Oriol Remeu", "Francisco Trincão", "Andre Gomes",
        "Marc Bartra", "Hector Bellerin", "Rafinha Alcántara", "Gerard Deulofeu", "Denis Suárez",
        "Thomas Vermaelen", "Todibo", "Neto", "Carles Perez", "Pablo Torre", "Inaki Pena", "Nelson Semedo", "Riqui Puig", "Clement Lenglet",
    ]
}
# Rarity probabilities
rarity_probabilities = {
    "Legendary": 0.05,  # 5% chance
    "Epic": 0.15,       # 15% chance
    "Rare": 0.30,       # 30% chance
    "Common": 0.50      # 50% chance
}

# Math quiz for earning money
def earn_money():
    """Present a math problem to earn money."""
    print("\nHow would you like your questions to be?:")
    print("1. Easy question ($50 reward)")
    print("2. Hard question ($100 reward)")
    difficulty = input("Select difficulty (1 or 2): ").strip()
    
    if difficulty not in ["1", "2"]:
        print("❌ Invalid choice. No money earned.")
        return 0

    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul
    }

    if difficulty == "1":
        # Easy question: Numbers between 1 and 10
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        reward = 50
    else:
        # Hard question: Numbers between 10 and 50, with an additional division option
        num1, num2 = random.randint(10, 50), random.randint(1, 10)
        operations["/"] = operator.truediv
        reward = 100

    op = random.choice(list(operations.keys()))
    if op == "/":
        num1 = num1 * num2  # Ensure clean division

    print(f"Solve this: {num1} {op} {num2}")
    try:
        answer = float(input("Your answer: ").strip())
        correct_answer = operations[op](num1, num2)
        # Accept rounded answers for division
        if abs(answer - correct_answer) < 0.01:
            print(f"✅ Correct! You earned ${reward}!")
            return reward
        else:
            print(f"❌ Incorrect! The correct answer was {correct_answer:.2f}. No money earned.")
            return 0
    except ValueError:
        print("❌ Invalid input! No money earned.")
        return 0

# Simulating pulls
def pull_player(guaranteed_epic=False, guaranteed_legendary=False, desired_player=None, guaranteed_desired=False):
    """Simulate a single gacha pull."""
    if guaranteed_desired:
        # If the guaranteed desired player condition is met, return the desired player
        for rarity, players in players_by_rarity.items():
            if desired_player in players:
                print(f"🔥 Guaranteed pull! You got your desired player: {desired_player} ({rarity})")
                return {"name": desired_player, "rarity": rarity}

    if guaranteed_legendary:
        rarity = "Legendary"
    elif guaranteed_epic:
        rarity = "Epic"
    else:
        # Select rarity based on probability
        rarity = random.choices(
            population=list(rarity_probabilities.keys()),
            weights=list(rarity_probabilities.values()),
            k=1
        )[0]

    # Get a random player from the selected rarity
    pulled_player = random.choice(players_by_rarity[rarity])

    # Simulating pull's animation
    print("⚽ Spinning the wheel...")
    time.sleep(1)
    print(f"🌟 {rarity.upper()} pull incoming!")
    time.sleep(1)
    print(f"🎉 Congratulations! You got: {pulled_player} ({rarity})")
    return {"name": pulled_player, "rarity": rarity}

# Perform multiple pulls with guarantees
def perform_pulls(num_pulls, desired_player=None, counters=None):
    """Perform multiple pulls with guarantees for desired Epic or Legendary players, including a pity counter."""
    if counters is None:
        counters = {
            "pulls_since_last_epic": 0,
            "pulls_since_last_legendary": 0,
            "pulls_since_desired": 0,
        }

    results = []

    # Determine the rarity of the desired player
    desired_rarity = None
    for rarity, players in players_by_rarity.items():
        if desired_player in players:
            desired_rarity = rarity
            break

    if desired_player and not desired_rarity:
        print(f"❌ {desired_player} is not a valid player in the system.")
        return results, counters

    # Display rarity-based pity thresholds
    if desired_rarity == "Epic":
        print(f"✨ Your desired player is Epic. Guaranteed after 39 pulls.")
    elif desired_rarity == "Legendary":
        print(f"🌟 Your desired player is Legendary. Guaranteed after 79 pulls.")

    for _ in range(num_pulls):
        # Define guarantees for desired player based on rarity
        guaranteed_desired_epic = (
            desired_rarity == "Epic" and counters["pulls_since_desired"] >= 39
        )
        guaranteed_desired_legendary = (
            desired_rarity == "Legendary" and counters["pulls_since_desired"] >= 79
        )
        guaranteed_desired = guaranteed_desired_epic or guaranteed_desired_legendary

        # Define general rarity guarantees
        guaranteed_epic = counters["pulls_since_last_epic"] >= 39
        guaranteed_legendary = counters["pulls_since_last_legendary"] >= 79

        # Simulate the pull
        player = pull_player(
            guaranteed_epic=guaranteed_epic,
            guaranteed_legendary=guaranteed_legendary,
            desired_player=desired_player,
            guaranteed_desired=guaranteed_desired,
        )
        results.append(player)

        # Update counters
        if player["name"] == desired_player:
            counters["pulls_since_desired"] = 0
        else:
            counters["pulls_since_desired"] += 1

        if player["rarity"] == "Legendary":
            counters["pulls_since_last_legendary"] = 0
        else:
            counters["pulls_since_last_legendary"] += 1

        if player["rarity"] in ["Epic", "Legendary"]:
            counters["pulls_since_last_epic"] = 0
        else:
            counters["pulls_since_last_epic"] += 1

        # Display pity counter progress
        print(f"\n🎰 Pull {_ + 1}")
        print(f"Pulled: {player['name']} ({player['rarity']})")
        print(f"General Epic Pity Counter: {counters['pulls_since_last_epic']}/39")
        print(f"General Legendary Pity Counter: {counters['pulls_since_last_legendary']}/79")

        if desired_player:
            if desired_rarity == "Epic":
                print(
                    f"Pity counter for {desired_player}: {counters['pulls_since_desired']}/39 "
                    f"({'Guaranteed next pull!' if counters['pulls_since_desired'] >= 39 else ''})"
                )
            elif desired_rarity == "Legendary":
                print(
                    f"Pity counter for {desired_player}: {counters['pulls_since_desired']}/79 "
                    f"({'Guaranteed next pull!' if counters['pulls_since_desired'] >= 79 else ''})"
                )

    return results, counters


# Main function to simulate gacha pulls
def main():
    money = 900  # Starting money
    pity_counters = {
        "pulls_since_last_epic": 0,
        "pulls_since_last_legendary": 0,
        "pulls_since_desired": 0,
    }

    print("""
    🌟 Welcome to Barcelona Gacha 🌟
    🎉 Collect the greatest players from Barcelona's history! 🎉
    """)

    while True:
        # Prompt for the desired player
        print("Enter the name of your desired player and press Enter to confirm.")
        print("Or type = and press Enter to skip selecting a desired player.")
        desired_player = input("Your desired player: ").strip()

        # Check if the user wants to skip
        if desired_player == "=":
            print("No desired player selected. Proceeding without a desired player.")
            desired_player = None
            break

        # Validate the entered player
        if not any(desired_player in players for players in players_by_rarity.values()):
            print(f"❌ {desired_player} is not a valid player in the system. Please try again.")
        else:
            print(f"✅ {desired_player} confirmed as your desired player!")
            break

    # Game loop 
    while True:
        print(f"\n💰 Your balance: ${money}")
        print("\nWhat would you like to do?:")
        print("1. Pull once ($10)")
        print("2. Pull 10 times ($90)")
        print("3. Earn money by solving math problems")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            if money < 10:
                print("❌ Not enough money! Solve math problems to earn more.")
                continue
            money -= 10
            results, pity_counters = perform_pulls(1, desired_player=desired_player, counters=pity_counters)
        elif choice == "2":
            if money < 90:
                print("❌ Not enough money! Solve math problems to earn more.")
                continue
            money -= 90
            results, pity_counters = perform_pulls(10, desired_player=desired_player, counters=pity_counters)
        elif choice == "3":
            money += earn_money()
            continue
        elif choice == "4":
            print("Thank you for playing Barcelona Gacha! ⚽")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        # Display results
        print("\n✨ Results ✨")
        for i, player in enumerate(results, start=1):
            print(f"Pull {i}: {player['name']} ({player['rarity']})")

        # Count and display rarity statistics
        rarity_count = {}
        for player in results:
            rarity_count[player['rarity']] = rarity_count.get(player['rarity'], 0) + 1

        print("\n📊 Summary 📊")
        for rarity, count in rarity_count.items():
            print(f"{rarity}: {count} players")


if __name__ == "__main__":
    main()
