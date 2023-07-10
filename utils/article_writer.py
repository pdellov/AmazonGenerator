import openai
from configparser import ConfigParser
import re
import json
import base64
from urllib.request import urlopen
import requests
from utils.amazon_scraper import amazonProduct

class articleWriter:
    def __init__(self):
            self.config_object = ConfigParser()
            self.config_object.read('config.ini')
            OPENAI = self.config_object["OPENAI"]
            self.key = OPENAI['apikey']
            self.language = OPENAI['lang']

    def openai_text(self,system_prompt,user_prompt,max_tokens):
        openai.api_key = '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'
        system_prompt = system_prompt + '. Remains in max ' + str(max_tokens) + 'chars while answering'
        text_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        text = text_response["choices"][0]["message"]["content"]
        return re.sub("-3\n\n", "", text)
    
    def write_fromproduct(self,product):
        print("Writing article about: " + str(product.name))
        product_data = "Product name: " + str(product.name) +\
            " - Product description: " + str(product.description) +\
            " - Product price:: " + str(product.price) +\
            " - Product details: " + str(product.details) +\
            " - Product reviews: " + str(product.reviews)
        product_url = str(product.url)
        system_prompt = "Agisci come un giornalista che recensisce articoli per lo sport outdoor,\
                a partire dalle recensioni lette online su quei prodotti e da altre informazioni\
                sul prodotto (senza però copiare testi già scritti da altri, ma ispirandosi ad essi).\
                Scrivi una recensione, in un lungo post da circa 1800 parole, sulle informazioni di prodotto \
                che ti vengono fornite -ispirati alle recensioni che ti fornisco ed esplodine i concetti ma non dire mai\
                che hai preso informazioni dalle recensioni (fai piuttosto tuoi i concetti lì espressi\
                e sintetizzali). Dividi la recensione in paragrafi ben titolati, se necessario. Per ogni\
                paragrafo esplodi bene i concetti, spiegandoli a fondo. Non usare mai la dicitura 'in conclusione'\
                e scrivi nel modo più naturale possibile.\
                Segui queste indicazioni:\
                Inizia direttamente con il testo dell'introduzione, senza nessun titolo\
                (l'introduzione sarà l'unico paragrafo senza titolo di paragrafo)\
                Non inserire il titolo dell'articolo.\
                I titoli dei paragrafi devono essere preceduti da <h2> e seguiti da </h2>\
                Utilizza eventualmente il markup HTML\
                Nel testo riporta due o tre volte una riga con scritto\
                'Se vuoi comprare NOMEPRODOTTO (sostitutisci con il nome) puoi farlo a questo link su Amazon',\
                senza le virgolette. Inserisci un link cliccabile in HTML intorno a quesa riga di rimando ad Amazon\
                che rimandi all'URL: " + product_url + ". Scrivi in lingua " + self.language
        user_prompt = product_data

        self.article = self.openai_text(system_prompt,user_prompt,9000)
        
    def eeatize(self):
        system_prompt = "Migliora questo articolo accorpando paragrafi (solo ove necessario) e approfondendo\
            i paragrafi che restano, seguendo i principi EEAT di Google."
        if self.article is not None:
             self.article = self.openai_text(system_prompt,self.article,100000)
        else:
             print('There is no article to make better')
    
    def generate_title(self):
        system_prompt = "Sei un sistema di titolazione di articoli. Prendi in input un testo\
            e ne definisci un titolo per un blog in lingua " + self.language
        if self.article is not None:
             self.title = self.openai_text(system_prompt,self.article,80).replace('"','')

    def extract_categories(self,data):
        output = ''
        for item in data:
            id = item.get('id')
            name = item.get('name')
            output += f'{name} - {id}\n'
        return output
    
    def wordpress_publish(self,image_url):
        if self.article is not None and self.title is not None:
            WORDPRESS = self.config_object["WORDPRESS"]
            wp_user = WORDPRESS['admin']
            wp_password = WORDPRESS['password']
            wp_url = WORDPRESS['url']
            wp_category = WORDPRESS['category_id']
            wp_connection = wp_user + ':' + wp_password
            token = base64.b64encode(wp_connection.encode())

            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}
            

            # First, download the image
            image_content = urlopen(image_url).read()
            # Then, upload the image to WordPress
            media = {'file': ('image.jpg', image_content)}
            response = requests.post(wp_url + '/wp-json/wp/v2/media', headers=headers, files=media)
            response_json = response.json()
            imageID = str(response_json['id'])

            try:
                # Estraggo la lista categorie
                response = requests.get(wp_url + '/wp-json/wp/v2/categories')
                data = response.json()
                categories = self.extract_categories(data)

                # Scelgo la categoria più adeguata
                system_prompt = "Sei un selezionatore di categorie\
                    Hai la seguente lista di categorie e ID e dato in input un titolo di un post\
                    scegli qual è la migliore categoria per quel post e restituisci in output\
                    l'ID di tale categoria (l'output deve essere solo ed esclusivamente l'ID della\
                    categoria). Qui la lista di categorie e relativi ID: " + categories
                wp_category = self.openai_text(system_prompt,self.article,50)
            except:
                pass


            # Then, create your post
            post = {
                'title': self.title,
                'status': 'publish',
                'content': self.article,
                'featured_media': imageID,
                'categories': wp_category,
                'author': '1',
                'format': 'standard'
            }

            # And finally, upload your post to WordPress
            response = requests.post(wp_url + '/wp-json/wp/v2/posts', headers=headers, json=post)

            # Check if the post was successful
            if response.status_code == 201:
                print("Post created successfully.")
            else:
                print(f"Failed to create post, status code: {response.status_code}.")   





         
                  
                
        

