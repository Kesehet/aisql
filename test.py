


import requests
import json

count = 0

def make_request(query, url = 'http://127.0.0.1:5000/request' , content_type='application/json'):
    global count
    count += 1
    headers = {'Content-Type': content_type}
    data = {'query': query}

    if content_type == 'application/x-www-form-urlencoded':
        response = requests.post(url, data=data, headers=headers)
    else:
        response = requests.post(url, json=data, headers=headers)
        
    save_to_html(f'<b>Query {count}:</b> {query}')
    try:
        resp = response.json()
        
        save_to_html(f'<b>Response {count}:</b>')
        save_to_html(f'<pre>{resp["query"]}</pre>', mode='a')
        save_to_html(f'''
                        <pre class="foldable">{json.dumps(resp["result"], indent=4)}</pre>
                        <button class="btn btn-primary" onclick="toggleFoldable(this)">See Response</button>
                    ''', mode='a')

    
    except Exception as e:
        print(f"Query {count}: {query}")
        print(f"Exception: {e}")
        save_to_html(f'<b>Response {count}:</b>')
        save_to_html(f'<pre>{str(e)}</pre>', mode='a')
    
    save_to_html(f'<hr>', mode='a')

    

def save_to_html(text, file_name='test_results.html', mode='a'):
    with open("test_results.html", mode) as f:
        f.write(text)
        f.write('<br>')



# Clear the test_results.html file
save_to_html('', 'test_results.html', 'w')

# Create a basic looking website structure and write it to html file using bootstrap.
save_to_html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <style>
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .foldable {
            display: block;
            width: 100%;
            overflow: hidden;
            max-height: 0;
            transition: max-height 0.5s ease-out;
        }
        .foldable.open {
            max-height: 1000px;
        }

    </style>
    
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Basic Website</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <meta http-equiv="refresh" content="60">
            
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center">SQL Query Results</h1>
            <hr>
             
    """)
    




### 🟪 **Combined Queries**


make_request('List the top 5 most reviewed products with average rating above 4.')
make_request('Find all users who reviewed more than one product with "organic" in the title.')
make_request('Show the average rating per sub_category_id for b2c products.')
make_request('List products reviewed by users from the same city as the product delivery area.')




### 🔄 Column Comparison Queries

make_request('Which products have b2c_price greater than b2b_price?')
make_request('List products where b2c_sale_price is higher than b2c_price.')
make_request('Find products where b2b_sale_price is less than b2b_price.')
make_request('Show all products where created_at is after updated_at.')
make_request('Which products have the same value for b2c_price and b2c_sale_price?')
make_request('Find products where b2b_min_quantity is less than 5 but b2b_sale_price is greater than b2c_sale_price.')
make_request('List products where the length of title is less than the length of description.')
make_request('Find products where delivery_time is greater than b2b_min_quantity.')
make_request('Which products have a higher discount percentage in b2b compared to b2c?')
make_request('List products where b2b_price and b2c_price are both null.')



### 🟩 **Pricing Queries**

make_request('What is the average b2c_price across all products?')
make_request('What is the maximum b2b_sale_price in the database?')
make_request('List products where b2c_sale_price is at least 20% lower than b2c_price.')
make_request('Show products where b2b_price is greater than b2c_price.')
make_request('Calculate average b2b_price per sub_category_id.')
make_request('Which products have a b2b_min_quantity greater than 100 and a b2b_sale_price under 50?')
make_request('Show the discount percentage between b2c_price and b2c_sale_price for all products.')
make_request('List all products where b2c_sale_price is null but b2c_price is not.')




### 🟨 **Filtering Queries**

make_request('Which products have "organic" in their description or title?')
make_request('Find products that do not belong to any sub_category_id.')
make_request('List all products where delivery_time is less than or equal to 2 days.')
make_request('Which products have free pickup available and belong to a specific main_category_id?')
make_request('Find products that belong to a certain product_type and have a gallery image.')
make_request('List all products where gallery is empty or null.')
make_request('Show all products with SKU starting with "ABC".')




### 🟦 **Time-based Queries**

make_request('List products created in the last 30 days.')
make_request('How many products were updated today?')
make_request('Find products created before 2024-01-01.')
make_request('Show all products where updated_at is greater than created_at.')
make_request('What is the average number of products added per month?')


### 🟥 **Count as Queries**
make_request('How many products have a b2b_price greater than 100?')
make_request('Count the number of products in each sub_category_id.')
make_request('How many products have a b2c_price less than 10 compared to b2b_price?')



### 🟩 **Cross-Table Filtering Queries**


make_request('List all reviews for products with "eco-friendly" in the title.')
make_request('Show all reviews written by users with role "customer".')
make_request('Find all users who have reviewed products in a specific sub_category_id.')
make_request('Which products with b2c_price under 20 have reviews from users in a specific city?')
make_request('List products that have at least one review and belong to a main_category_id = 5.')
make_request('Find users who reviewed a product but haven’t verified their email.')
make_request('List all reviews for products with b2b_min_quantity greater than 100.')




### 🟦 **Cross-Table Time-based Queries**


make_request('List reviews created in the last 7 days for products in sub_category_id = 10.')
make_request('Which users created accounts after writing a review?')
make_request('Find all products reviewed before 2024-01-01.')
make_request('List products that were reviewed within 3 days of being created.')
make_request('Find users who left a review within 24 hours of account creation.')




### 🟥 **Cross-Table Count Queries**


make_request('How many reviews were made per product?')
make_request('Count the number of products reviewed by each user.')
make_request('How many users have reviewed more than 5 products?')
make_request('Which product has the highest number of reviews?')
make_request('How many reviews were made by users with role "admin"?')
make_request('Count how many products in each sub_category_id have at least one review.')






save_to_html("""""
             
        </div>
        <footer class="bg-light text-center text-lg-start mt-5">
            <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
                Made with <3 by <a class="text-dark" href="https://github.com/Kesehet/">Kesehet</a>
            </div>
        </footer>
             
            
        <script>
        function toggleFoldable(button) {
            const foldable = button.previousElementSibling;
            foldable.classList.toggle('open');
        }

        </script>
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>""")