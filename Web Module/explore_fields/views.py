from django.shortcuts import render
import json
import os
import requests

def explore_fields(request):
    newsapi_key = 'ea2b2ad73b844acf9b29b58c9fd2646f'  # Replace with your NewsAPI API key
    categories = ['technology', 'general', 'business', 'entertainment', 'health', 'science', 'sports']
    articles_by_category = {}

    for category in categories:
        url = f'https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={newsapi_key}'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            articles = data.get('articles', [])
            for article in articles:
                image_url = article.get('urlToImage')
                article['image_url'] = image_url
            articles_by_category[category] = articles[:10]  # Fetch the top 10 articles for each category
        else:
            # If API result is not available, try fetching data from saved file
            file_path = f'D:/Project/Website-Phoenix13/LearnersEd/explore_fields/news/{category}.json' 
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 0:
                    with open(file_path, 'r') as file:
                        articles = json.load(file)
                        articles_by_category[category] = articles
                else:
                    error_message = 'Error Fetch: Not able to fetch articles'
                    context = {'error_message': error_message}
                    return render(request, 'error.html', context)
            else:
                error_message = data.get('message', 'Error File: File Not Found')
                context = {'error_message': error_message}
                return render(request, 'error.html', context)

    # Save the fetched data to files
    for category, articles in articles_by_category.items():
        file_path = f'D:/Project/Website-Phoenix13/LearnersEd/explore_fields/news/{category}.json'
        with open(file_path, 'w') as file:
            json.dump(articles, file)

    context = {'articles_by_category': articles_by_category}
    return render(request, 'news_list.html', context)
