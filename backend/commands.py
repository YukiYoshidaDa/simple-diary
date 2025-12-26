import click
from flask.cli import with_appcontext

from extensions import db
from services import post_service, user_service


@click.command(name="seed")
@with_appcontext
def seed():
    """Seed the database with sample data."""
    # Reset DB (optional, be careful in production!)
    db.drop_all()
    db.create_all()

    click.echo("Database reset.")

    # Create Users
    user1 = user_service.register_user(
        {"username": "yuki", "email": "yuki@example.com", "password": "password"}
    )

    user2 = user_service.register_user(
        {"username": "testuser", "email": "test@example.com", "password": "password"}
    )
    click.echo(f"Created users: {user1.username}, {user2.username}")

    # Create Posts
    post_service.create_post({"content": "Hello, Simple Diary!"}, user1.id)
    post_service.create_post({"content": "This is my first post."}, user1.id)
    post_service.create_post({"content": "Another day, another bug fixed."}, user1.id)

    post_service.create_post(
        {"content": "Frontend development starting soon."}, user2.id
    )

    click.echo("Created sample posts.")
    click.echo("Seeding complete!")
