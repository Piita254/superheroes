from random import choice as rc
from app import app
from models import db, Hero, Power, SuperHero

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        # Clear out the existing data from the database
        SuperHero.query.delete()
        Power.query.delete()
        Hero.query.delete()

        print("Seeding powers...")
        # Seed powers (description only, no name field as per the original model)
        powers = [
            Power(description="Gives the wielder super-human strength."),
            Power(description="Gives the wielder the ability to fly at supersonic speed."),
            Power(description="Allows the wielder to use their senses at a super-human level."),
            Power(description="Can stretch the human body to extreme lengths."),
        ]
        db.session.add_all(powers)

        print("Seeding heroes...")
        # Seed heroes (name and super_name fields as per the original model)
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.add_all(heroes)

        print("Assigning powers and strength levels to heroes...")
        # Assign random powers and strengths to heroes
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []

        for hero in heroes:
            power = rc(powers)  # Assign a random power to each hero
            hero_powers.append(
                SuperHero(hero=hero, power=power, strength=rc(strengths))
            )

        db.session.add_all(hero_powers)
        db.session.commit()

        print("Done seeding!")
