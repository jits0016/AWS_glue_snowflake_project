#!/usr/bin/env python
# coding: utf-8

# In[2]:




# In[1]:


import requests
import nltk
import re


# In[1]:

# In[2]:
import boto3
# In[4]:
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from config import API_KEY

# In[5]:

def get_movie_data(i):
    response=requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key={}&&language=en-US&page={}'.format(API_KEY,i))
    Jsondata=response.json()['results']
    return Jsondata
# In[6]:
def concat_data():
   initial_df=pd.DataFrame()
   for i in range(1,567):
      Jsondata=get_movie_data(i)
      df=pd.DataFrame(Jsondata)
      temp_df=df[['id','title','overview','release_date','popularity','vote_average','vote_count']]
      initial_df=initial_df.append(temp_df,ignore_index=True)
      return initial_df

# In[7]:

# Function to clean text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    return text

# In[8]:

# Function to remove stopwords
def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# In[11]:


def transform_data(final_df):
   # Filter out movies with a popularity score greater than 20
   # and vote count greater than 300
   filtered_df = final_df[(final_df['popularity'] > 20) & (final_df['vote_count'] > 300)]

   # sort the movies based on popularity in descending order
   sorted_df = filtered_df.sort_values(by='popularity', ascending=False)

   # Remove Duplicate Rows
   deduplicated_df = sorted_df.drop_duplicates()

   # Drop Rows with Missing Values
   cleaned_df = deduplicated_df.dropna()

   # Convert Data Types (if needed)
   cleaned_df['release_date'] = pd.to_datetime(cleaned_df['release_date'])

   # Text Data Cleaning (Overview Column)
   cleaned_df['overview'] = cleaned_df['overview'].apply(clean_text)
   cleaned_df['overview'] = cleaned_df['overview'].apply(remove_stopwords)

   # Rename Columns
   cleaned_df.rename(columns={'original_title': 'title', 'vote_average': 'avg_vote','overview':'Movie Overview'}, inplace=True)

   # Joining with Additional Data
   # For example, let's say you have a DataFrame with genre information
   genres_data = pd.DataFrame(...)  # Load your genre data here
   cleaned_df = cleaned_df.merge(genres_data, on='genre_id', how='left')
   
   #create current date column
   cleaned_df['todays_date'] = datetime.today().date()
   return cleaned_df


# In[12]:


def write_data_to_s3(cleaned_df):
   # Convert DataFrame to CSV format
   csv_buffer = io.StringIO()
   cleaned_df.to_csv(csv_buffer, index=False)

   # Initialize the S3 client
   s3_client = boto3.client('s3')

   # Upload CSV content to S3
   s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=jjitu2023, Key=tmdb_cleaned_data/tmdb.csv)

   print("CSV file uploaded to S3 successfully.")


# In[13]:


def lambda_handler(event,context):
    df1=concat_data()
    # Download stopwords if not already downloaded
    nltk.download('stopwords')
    nltk.download('punkt')
    cleaned_data=transform_data(df1)
    write_data_to_s3(cleaned_df)


# In[15]:
