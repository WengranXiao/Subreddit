from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('flasktry.html')
    
@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    
    from final_project import tree

    answer1 = request.form["answer1"]
    answer2 = request.form["answer2"]

    if answer1=='yes':
        tree=tree[1]
    else:
        tree=tree[2]

    if answer2=='yes':
        tree=tree[1]
    else:
        tree=tree[2]


    return render_template('response.html', list=tree[0])
    
    
    
if __name__ == "__main__":
    app.run(debug=True) 