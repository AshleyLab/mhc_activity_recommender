from flask import Flask, render_template, flash
import create_mysql_db
from update_user import update_user_main_helper
from recommend import recomend_main_helper
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/init")
def init():
    create_mysql_db.main()
    flash("DB Initalized")
    return render_template('index.html')

@app.route("/pref")
def pref():
    user="testuser"
    user_pref_file = "test_feature_sets/test_feature_ranks.tsv"
    user_fitness_level = 3
    update_user_main_helper(user, user_pref_file, user_fitness_level)
    flash("Loaded features from fetest_feature_ranks.tsv and fitness level = 3")
    return render_template('index.html')

@app.route("/recommendations")
def recommendations():
    #recommendations_lifestyle = recomend_main_helper("testuser", "lifestyle", 3) # Does not run
    #recommendations_training = recomend_main_helper("testuser", "training", 3)
    recommendations_video = recomend_main_helper("testuser", "videos", 3)
    #flash(set(recommendations_video))
    print (recommendations_video)
    return render_template('index.html', recommendations=recommendations_video)

if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()