
import telebot
import requests
from deep_translator import GoogleTranslator

bot = telebot.TeleBot()
api = 


keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
search_button = telebot.types.KeyboardButton()
best_movies_button = telebot.types.KeyboardButton()
best_series_button = telebot.types.KeyboardButton()
keyboard.add(search_button, best_movies_button, best_series_button)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, , reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == )
def search(message):
    bot.reply_to(message, )

@bot.message_handler(func=lambda message: message.text == '')
def best_movies(message):
    movie_url = f"api"
    try:
        movie_response = requests.get(movie_url).json()
    except requests.exceptions.RequestException as e:
        error_message = f"Sorry, there was an error: {str(e)}"
        bot.reply_to(message, error_message)
        print(error_message)
        return

    response_text = "Here are the top 50 best rated movies:\n\n"
    for i, movie in enumerate(movie_response["results"][:50]):
        response_text += f"{i+1}. {movie['title']} ({movie['release_date'][:4]})\n"

    bot.reply_to(message, response_text)
@bot.message_handler(func=lambda message: message.text == '')
def best_series(message):
    series_url = f"https://api"
    series_response = requests.get(series_url).json()

    response_text = "Here are the top 20 best rated TV series:\n\n"
    for i, series in enumerate(series_response["results"][:50]):
        response_text += f"{i+1}. {series['name']} ({series['first_air_date'][:4]})\n"

    bot.reply_to(message, response_text)

@bot.message_handler(func=lambda message: True)
def find_movie_or_series(message):
    search_query = message.text + "."
    search_url = f"https://api&query={search_query}"
    response = requests.get(search_url).json()

    if response["total_results"] == 0:
        bot.reply_to(message, "Sorry, no results found ")
    else:
        result = response["results"][0]

        if result["media_type"] == "movie":
            movie_id = result["id"]
            movie_url = f"https://api"
            movie_response = requests.get(movie_url).json()


            similar_url = f"https://api"
            similar_response = requests.get(similar_url).json()

            title = movie_response["title"]
            overview = movie_response["overview"]
            genres = [genre["name"] for genre in movie_response["genres"]]
            director = None
            if "credits" in movie_response:
                director = [crew["name"] for crew in movie_response["credits"]["crew"] if crew["job"] == "Director"]
            imdb_rating = movie_response["vote_average"]
            release_date = movie_response["release_date"]
            runtime = movie_response["runtime"]
            poster_path = movie_response["poster_path"]
            poster_url = f"api{poster_path}"


            translator = GoogleTranslator(source='auto', target='fa')
            title_fa = translator.translate(title)
            overview_fa = translator.translate(overview)
            genres_fa = [translator.translate(genre) for genre in genres]
            director_fa = None
            if director:
                director_fa = [translator.translate(director[0])]
            imdb_rating_fa = translator.translate(f"{imdb_rating}/10")
            release_date_fa = translator.translate(release_date)
            runtime_fa = translator.translate(f"{runtime} minutes")

            
            response_text = f"*{title_fa}*\n\n"
            response_text += f"🎞 ژانر: {', '.join(genres_fa)}\n"
            if director_fa:
                response_text += f"🎥 کارگردان: {director_fa[0]}\n"
            response_text += f"⭐️ نمره: {imdb_rating_fa}\n"
            response_text += f"📅 تاریخ پخش: {release_date_fa}\n"
            response_text +=   f"▶️ مدت: {runtime_fa}\n\n"
            response_text += f"{overview_fa}\n\n"
            response_text += f"میتونی از اینجا دانلود کنی: "
            bot.send_photo(message.chat.id, photo=poster_url, caption=response_text, parse_mode="Markdown")

            # Send similar movies
            if len(similar_response["results"]) > 0:
                response_text = f"🎬 *فیلم های مشابه:*\n\n"
                for movie in similar_response["results"][:5]:
                    response_text += f"{movie['title']} ({movie['release_date'][:4]})\n"
                bot.reply_to(message, response_text, parse_mode="Markdown")
        elif result["media_type"] == "tv":
            series_id = result["id"]
            series_url = f"https://api{series_id}?api_key={api}&append_to_response=credits"
            series_response = requests.get(series_url).json()

           
            similar_url = f"api{series_id}/similar?api_key={api}"
            similar_response = requests.get(similar_url).json()

            name = series_response["name"]
            overview = series_response["overview"]
            genres = [genre["name"] for genre in series_response["genres"]]
            creator = [creator["name"] for creator in series_response["created_by"]]
            imdb_rating = series_response["vote_average"]
            first_air_date = series_response["first_air_date"]
            episode_run_time = series_response["episode_run_time"][0]
            poster_path = series_response["poster_path"]
            poster_url = f"https://image.tmdb.org/t/p/original{poster_path}"

           
            translator = GoogleTranslator(source='auto', target='fa')
            name_fa = translator.translate(name)
            overview_fa = translator.translate(overview)
            genres_fa = [translator.translate(genre) for genre in genres]
            creator_fa = []
            if creator:
               creator_fa = [translator.translate(creator[0])]
            imdb_rating_fa = translator.translate(f"{imdb_rating}/10")
            first_air_date_fa = translator.translate(first_air_date)
            episode_run_time_fa = translator.translate(f"{episode_run_time} minutes")

            response_text = f"*{name_fa}*\n\n"
            response_text += f"🎞 ژانر: {', '.join(genres_fa)}\n"
            response_text += f"🎥 کارگردان: {creator_fa[0]}\n"
            response_text += f"⭐️ نمره: {imdb_rating_fa}\n"
            response_text += f"📅 تاریخ پخش: {first_air_date_fa}\n"
            response_text += f"▶️ مدت زمان هر قسمت: {episode_run_time_fa} \n\n"
            response_text += f"{overview_fa}\n\n"
            response_text += f"میتونی از اینجا دانلود کنی: filmkio.run/series"
            bot.send_photo(message.chat.id, photo=poster_url, caption=response_text, parse_mode="Markdown")

        
            if len(similar_response["results"]) > 0:
                response_text = f"🎬 *سریال های مشابه:*\n\n"
                for series in similar_response["results"][:5]:
                    response_text += f"{series['name']} ({series['first_air_date'][:4]})\n"
                bot.reply_to(message, response_text, parse_mode="Markdown")

bot.polling()

