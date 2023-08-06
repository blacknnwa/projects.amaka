import boto3

# Initialize AWS clients
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

# DynamoDB table name
table_name = input("Enter the table name: ")

def create_table():
    # Code to create the DynamoDB table
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'property_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'property_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("DynamoDB table created successfully!")
    except Exception as e:
        print("Error creating DynamoDB table:", str(e))

def upload_file(file_path, bucket_name):
    # Code to upload a file to S3 bucket
    try:
        with open(file_path, 'rb') as file:
            s3.upload_fileobj(file, bucket_name, file_path)
        print("File uploaded successfully!")
    except Exception as e:
        print("Error uploading file:", str(e))

def download_file(file_name, bucket_name):
    # Code to download a file from S3 bucket
    try:
        s3.download_file(bucket_name, file_name, file_name)
        print("File downloaded successfully!")
    except Exception as e:
        print("Error downloading file:", str(e))

def add_property():
    # Code to add a property to the portfolio in DynamoDB
    try:
        property_id = input("Enter the property ID: ")
        address = input("Enter the property address: ")
        purchase_price = float(input("Enter the purchase price: "))
        monthly_rent = float(input("Enter the monthly rent: "))
        expenses = float(input("Enter the monthly expenses: "))

        item = {
            'property_id': {'S': property_id},
            'address': {'S': address},
            'purchase_price': {'N': str(purchase_price)},
            'monthly_rent': {'N': str(monthly_rent)},
            'expenses': {'N': str(expenses)}
        }

        dynamodb.put_item(
            TableName=table_name,
            Item=item
        )
        print("Property added successfully!")
    except Exception as e:
        print("Error adding property:", str(e))

def remove_property():
    # Code to remove a property from the portfolio in DynamoDB
    property_id = input("Enter the property ID to remove: ")

    try:
        dynamodb.delete_item(
            TableName=table_name,
            Key={
                'property_id': {'S': property_id}
            }
        )
        print("Property removed successfully!")
    except Exception as e:
        print("Error removing property:", str(e))

def list_properties():
    # Code to list all properties in the portfolio from DynamoDB
    try:
        response = dynamodb.scan(
            TableName=table_name
        )
        properties = response['Items']

        if not properties:
            print("No properties found in the portfolio.")
        else:
            print("Properties in the portfolio:")
            for property in properties:
                property_id = property['property_id']['S']
                address = property['address']['S']
                purchase_price = float(property['purchase_price']['N'])
                monthly_rent = float(property['monthly_rent']['N'])
                expenses = float(property['expenses']['N'])

                print(f"Property ID: {property_id}")
                print(f"Address: {address}")
                print(f"Purchase Price: {purchase_price}")
                print(f"Monthly Rent: {monthly_rent}")
                print(f"Expenses: {expenses}")
                print()

    except Exception as e:
        print("Error listing properties:", str(e))

def calculate_roi():
    # Code to calculate the return on investment for a property
    property_id = input("Enter the property ID to calculate ROI: ")

    try:
        response = dynamodb.get_item(
            TableName=table_name,
            Key={
                'property_id': {'S': property_id}
            }
        )
        item = response['Item']

        if not item:
            print("Property not found.")
        else:
            purchase_price = float(item['purchase_price']['N'])
            monthly_rent = float(item['monthly_rent']['N'])
            expenses = float(item['expenses']['N'])

            total_investment = purchase_price
            monthly_profit = monthly_rent - expenses

            roi = (monthly_profit * 12) / total_investment * 100

            print(f"ROI for Property ID {property_id}: {roi:.2f}%")

    except Exception as e:
        print("Error calculating ROI:", str(e))

def exit_program():
    # Code to exit the program
    print("Exiting the Real Estate Investments Portfolio Application.")
    exit()

def main_menu():
    print("Welcome to the Real Estate Investments Portfolio Application!")
    print("Please select an option:")
    print("1. Add Property")
    print("2. Remove Property")
    print("3. List Properties")
    print("4. Calculate ROI")
    print("5. Upload File to S3 Bucket")
    print("6. Download File from S3 Bucket")
    print("0. Exit")

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            add_property()
        elif choice == '2':
            remove_property()
        elif choice == '3':
            list_properties()
        elif choice == '4':
            calculate_roi()
        elif choice == '5':
            # Prompt user for file path and bucket name
            file_path = input("Enter the file path: ")
            bucket_name = input("Enter the S3 bucket name: ")
            upload_file(file_path, bucket_name)
        elif choice == '6':
            # Prompt user for file name and bucket name
            file_name = input("Enter the file name: ")
            bucket_name = input("Enter the S3 bucket name: ")
            download_file(file_name, bucket_name)
        elif choice == '0':
            exit_program()
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    # Create the DynamoDB table
    create_table()
    # Start the main menu
    main_menu()
