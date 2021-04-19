from flask import Flask, render_template, request
import pickle
import pandas as pd
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)


#########################
## FUNCTION FOR GRAPH ##
#########################

## IMPORT DATA USING pd.read_csv
df = pd.read_csv('FINAL\dashboard\static\df_for_graph.csv')

def category_plot(
    cat_plot = 'histplot',
    cat_x = 'hotel', cat_y = 'adr',
    estimator = 'count', hue = 'is_canceled'):

    df = pd.read_csv('FINAL\dashboard\static\df_for_graph.csv')

    if cat_plot == 'histplot':
        data = []
        for val in df[hue].unique():
            hist = go.Histogram(
                x=df[df[hue]==val][cat_x],
                y=df[df[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            data.append(hist)
        title='Histogram'

    if cat_plot == 'histplot':
        layout = go.Layout(
            title='Histogram',
            xaxis=dict(title=cat_x),
            yaxis=dict(title='total bookings'),
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title='Histogram',
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            boxmode = 'group'
        )

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def pie_plot(hue = 'is_canceled'):

    vcounts = df[hue].value_counts()     # Count Values ada berapa
    labels = []
    values = []
    for item in vcounts.iteritems():
        labels.append(item[0])             # append labels
        values.append(item[1])             # append values
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie Charts', title_x= 0.48)
    result = {'data': data, 'layout': layout}
    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

#########################

# HOME
@app.route('/')
def home():
    return render_template('home.html')

# DATASET
@app.route('/database', methods=['POST', 'GET'])
def database ():
    dataset = pd.read_csv('FINAL\dashboard\static\df_display.csv')
    dataArray = [dataset.columns.values.tolist()] + dataset.values.tolist()
    return render_template('dataset.html', dataArray = dataArray, row = len(dataArray), col = len(dataArray[0]))

# VISUALIZATION    
@app.route('/visualize', methods=['POST', 'GET'])
def index():
    plot = category_plot()

    list_plot = [('histplot', 'Histogram')]
    list_x = [('hotel', 'Hotel'),('distribution_channel', 'Booking Channel'), ('assigned_room_type', 'Room Type'), ('customer_type', 'Customer Type'), ('arrival_date_month','Month of Arrival')]
    list_y = [('adr', 'Price'), ('lead_time', 'Lead Time')]
    list_est = [('count', 'Count'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('hotel', 'Hotel'), ('is_canceled', 'Cancelled')]

    return render_template(
        'category.html',
        plot=plot,
        focus_plot='histplot',
        focus_x='hotel',
        focus_estimator='count',
        focus_hue='is_canceled',
        drop_plot= list_plot,
        drop_x= list_x,
        drop_y= list_y,
        drop_estimator= list_est,
        drop_hue= list_hue)
@app.route('/cat_fn/<nav>')
def cat_fn(nav):
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'distribution_channel'
        cat_y = 'adr'
        estimator = 'count'
        hue = 'is_canceled'

    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    if estimator == None:
        estimator = 'count'

    if cat_y == None:
        cat_y = 'hotel'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram')]
    list_x = [('hotel', 'Hotel'),('distribution_channel', 'Booking Channel'), ('assigned_room_type', 'Room Type'), ('customer_type', 'Customer Type'), ('arrival_date_month','Month of Arrival')]
    list_y = [('adr', 'Price'), ('lead_time', 'Lead Time')]
    list_est = [('count', 'Count'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('hotel', 'Hotel'), ('is_canceled', 'Cancelled')]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        'category.html',
        plot=plot,
        focus_plot=cat_plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_estimator=estimator,
        focus_hue=hue,
        drop_plot= list_plot,
        drop_x= list_x,
        drop_y= list_y,
        drop_estimator= list_est,
        drop_hue= list_hue
    )
@app.route('/visualize/pie_fn')
def pie_fn():
    hue = request.args.get('hue')
    if hue == None:
        hue = 'is_canceled'
    list_hue = [('is_canceled', 'Cancelled'), ('distribution_channel', 'Booking Channel'),('customer_type', 'Customer Type')]
    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)

# PREDICTION
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    return render_template('predict.html')

# RESULT
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        user = request.form.to_dict()

        print(user)

        df_to_predict = pd.DataFrame({
            'hotel': [user['hotel']],
            'lead_time': [user['lead_time']],
            'arrival_date_month': [user['arrival_date_month']],
            'arrival_date_day_of_month': [user['arrival_date_day_of_month']],
            'stays_in_weekend_nights': [user['stays_in_weekend_nights']],
            'stays_in_week_nights': [user['stays_in_week_nights']],
            'meal': [user['meal']],
            'distribution_channel': [user['distribution_channel']],
            'is_repeated_guest': [user['is_repeated_guest']],
            'previous_cancellations': [user['previous_cancellations']],
            'previous_bookings_not_canceled': [user['previous_bookings_not_canceled']],
            'assigned_room_type': [user['assigned_room_type']],
            'booking_changes': [user['booking_changes']],
            'agent': [user['agent']],
            'days_in_waiting_list': [user['days_in_waiting_list']],
            'customer_type': [user['customer_type']],
            'adr': [user['adr']],
            'required_car_parking_spaces': [user['required_car_parking_spaces']],
            'total_of_special_requests': [user['total_of_special_requests']],
            'total_guests': [user['total_guests']],
            'countries': [user['countries']]
        })

        prediksi = model.predict_proba(df_to_predict)

        if prediksi[:,1] >= 0.590833:
            quality = 'The Booking is likely to be CANCELLED'
        else:
            quality = 'The Guest is likely to COME'
        
        print(prediksi[:,1])


        return render_template('result.html', data=user, pred=quality)


if __name__ == '__main__':

    filename = 'FINAL/finalmodelRFCfit.sav'
    model = pickle.load(open(filename, 'rb'))

    app.run(debug=True, port=5000)