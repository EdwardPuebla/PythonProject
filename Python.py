# -*- coding: utf-8 -*-
"""Python
"""

# This will create a tool that trains several machine learning models to perform the task of classifying online reviews.
import json, requests, sklearn.tree, sklearn.metrics, sklearn.neighbors, sklearn.neural_network, math, sklearn.model_selection, textblob, nltk, joblib
nltk.download("punkt")

response = requests.get("https://dgoldberg.sdsu.edu/515/appliance_reviews.json")

if response:
    data = json.loads(response.text)
    
    unique = []
    #The code below will append and create a list of all the unique words 
    for line in data:
        review = line["Review"]
        review_word = textblob.TextBlob(review)

        for word in review_word.words:

            if word.lower() not in unique:
                unique.append(word.lower())
    #Below are the counters for narrowing down which words are relevant for classification 
    total = []            
    for word in unique:
        a = 0
        b = 0
        c = 0
        d = 0
        #Below will go through each word and count which they fall into.The counters are above   
        for line in data:
            
            if word in line["Review"].lower() and line["Safety hazard"] == 1:
                a+=1
            
            if word in line["Review"].lower() and line["Safety hazard"] == 0:
                b+=1

            if word not in line["Review"].lower() and line["Safety hazard"] == 1:
                c+=1

            if word not in line["Review"].lower() and line["Safety hazard"] == 0:
                d+=1
        #This will generate the relevance the score for the words, if there is an error of denominator of zero, then a relevance score of zero will be used for that word
        try:
            score = (math.sqrt(a + b + c + d)) * ((a * d) - (c * b)) / math.sqrt((a + b) * (c + d))
                
        except:
            score = 0
          
        if score >= 4000:

            total.append(word)
    #Below are the 2D list to train the machine learning models based on relevant words
    x = [] 
    y = []       
    for line in data:
        inner_list = []

        for word in total:

            if word in line["Review"].lower():
                inner_list.append(1)

            if word not in line["Review"].lower():
                inner_list.append(0)

        x.append(inner_list)
        y.append(line["Safety hazard"])


    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.2)

    #This will print the decision tree model
    dt_clf = sklearn.tree.DecisionTreeClassifier()
    dt_clf = dt_clf.fit(x_train, y_train)
    dt_predictions = dt_clf.predict(x_test)
    dt_accuracy = sklearn.metrics.accuracy_score(y_test, dt_predictions)
    print("Decision Tree accuracy:", dt_accuracy)

    #This will print the k-nearest neighbors model
    knn_clf = sklearn.neighbors.KNeighborsClassifier(5)
    knn_clf = knn_clf.fit(x_train, y_train)
    knn_predictions = knn_clf.predict(x_test)
    knn_accuracy = sklearn.metrics.accuracy_score(y_test, knn_predictions)
    print("k-nearest neighbors accuracy:", knn_accuracy)

    #This will print the neural network model
    nn_clf = sklearn.neural_network.MLPClassifier()
    nn_clf = nn_clf.fit(x_train, y_train)
    nn_predictions = nn_clf.predict(x_test)
    nn_accuracy = sklearn.metrics.accuracy_score(y_test, nn_predictions)
    print("Neural Network accuracy:", nn_accuracy)

    #This will determine the most accurate data and then print the most accurate data from the three models to be saved.
    most_accurate = {"Decision Tree model performed best;": dt_accuracy, "k-nearest neighbors model performed best;": knn_accuracy, "Neural Network model performed best;": nn_accuracy}
    best = max(most_accurate, key=most_accurate.get)

    print(best, "saved to model.joblib.")
    
    #Below will save the most accurate model 
    most_accurate_save = [dt_accuracy, knn_accuracy, nn_accuracy]
    save = max(most_accurate_save)
    
    if dt_accuracy > knn_accuracy and nn_accuracy:
        joblib.dump(dt_clf, "model.joblib")

    elif knn_accuracy > dt_accuracy and nn_accuracy:
        joblib.dump(knn_clf, "model.joblib")

    elif nn_accuracy > dt_accuracy and knn_accuracy:
        joblib.dump(nn_clf, "model.joblib")

    else:
        print("Sorry, error saving")

else:
    print("Sorry, error")
