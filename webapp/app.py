import flask
import pickle
import pandas as pd
import gensim
import nltk
#nltk.download('punkt')
import gcsfs

class tfModel():
    '''
    Usage:
        import pandas as pd
        import gensim
        ...
        m = tfModel('questions_with_tags.csv')
        query = 'Programming languages supporting functional programming'
        similar_documents = m.get_similar_documents(query, num_results=10)
    '''
    def __init__(self, question_file):
        qs = pd.read_csv(question_file)
        qs = qs.fillna(value={'new_tags': ''})
        raw_documents = qs['title'] + qs['new_tags']
        # sample to smaller number of documents
        raw_documents = raw_documents
        qs = qs
        self.questions = qs
        tokenized_docs = [[w.lower() for w in nltk.word_tokenize(text)] 
                            for text in raw_documents]
        self.dictionary = gensim.corpora.Dictionary(tokenized_docs)
        corpus = [self.dictionary.doc2bow(tokenized_doc) for tokenized_doc in tokenized_docs]
        tf_idf = gensim.models.TfidfModel(corpus)
        self.tf_idf = tf_idf
        self.similarity_checker = gensim.similarities.Similarity("",self.tf_idf[corpus],num_features=len(self.dictionary))

    def get_similar_documents(self, query, num_results=5, threshold=0.10):
        tokenized_query = [w.lower() for w in nltk.word_tokenize(query)]
        query_bag_of_words = self.dictionary.doc2bow(tokenized_query)
        query_tf_idf = self.tf_idf[query_bag_of_words]
        question_similarities = self.similarity_checker[query_tf_idf]
        print("Q Similarities", len(question_similarities), question_similarities)

        # Display similar questions from the past:

        questions_copy = self.questions.copy()
        questions_copy['similarity'] = question_similarities
        questions_above_threshold_similarity = questions_copy[questions_copy['similarity'] >= threshold]
        questions_above_threshold_similarity = questions_above_threshold_similarity.sort_values('similarity',ascending=False)

        fs = gcsfs.GCSFileSystem(project='w210-jcgy-254100')
        with fs.open('w210-jcgy-bucket/w210-data-output-new-q-and-a-files-with-separate-cleaned-answer-bodies/PostAnswersFiltered_V4_cleaned_answer_bodies.tsv', 'rb') as f:
        	answers = pd.read_csv(f, sep='\t')

        combined = pd.merge(questions_above_threshold_similarity, answers, how='left', left_on = 'accepted_answer_id', right_on = 'id')

        return (combined['title_x'].head(num_results), combined['cleaned_body'].head(num_results), combined['images_list'].head(num_results), combined['code_snippets'].head(num_results))

#m = tfModel('new_qs.csv')

fs = gcsfs.GCSFileSystem(project='w210-jcgy-254100')
with fs.open('w210-jcgy-bucket/w210-data-output-new-q-and-a-files-with-separate-cleaned-answer-bodies/new_qs.csv', 'rb') as f:
	m = tfModel(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        # Extract the input
        userquery = flask.request.form['userquery']

        # Make DataFrame for model
        input_variables = userquery

        # Get the model's prediction
        #prediction = model.predict(input_variables)[0]

        similar_que, similar_ans, similar_img, similar_code = m.get_similar_documents(input_variables, num_results=3)

        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('result.html',
                                     original_input=userquery,
                                     que=similar_que,
                                     ans=similar_ans,
				     img=similar_img,
				     code=similar_code,
                                     )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
