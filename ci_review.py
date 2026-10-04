import argparse
from parser import parse_plan
from ai import generate_review


def main():
    parser = argparse.ArgumentParser(
        description="AI Terraform Plan Review"
    )

    parser.add_argument(
        "--plan",
        required=True,
        help="Path to Terraform plan JSON file"
    )

    args = parser.parse_args()

    # Parse Terraform plan
    resources = parse_plan(args.plan)

    if not resources:
        print("No Terraform resource changes found.")
        return

    # Generate AI review
    review = generate_review(resources)

    print(review)


if __name__ == "__main__":
    main()