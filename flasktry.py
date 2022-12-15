from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    
    from final_project import tree

    answer1 = request.form["answer1"]
    answer2 = request.form["answer2"]
    answer3 = request.form["answer3"]
    answer4 = request.form["answer4"]
    answer5 = request.form["answer5"]

    if answer1=='yes':
        tree=tree[1]
    else:
        tree=tree[2]

    if answer2=='yes':
        tree=tree[1]
    else:
        tree=tree[2]

    if answer3=='yes':
        tree=tree[1]
    else:
        tree=tree[2]
        
    if answer4=='yes':
        tree=tree[1]
    else:
        tree=tree[2]
    if answer5=='yes':
        tree=tree[1]
    else:
        tree=tree[2]

    if tree[0]==[]:
        return render_template('response2.html')
    else:
        return render_template('response.html', list=tree[0])
    
    
    
if __name__ == "__main__":
    app.run(debug=True) 