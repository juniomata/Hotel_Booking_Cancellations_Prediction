# Hotel Booking Cancellations Prediction

__In the hospitality industry, demand forecast accuracy is highly impacted by booking cancellations__, which makes demand management decisions difficult and risky. In attempting to minimize losses, hotels tend to implement restrictive cancellation policies and employ overbooking tactics, which, in turn, reduce the number of bookings and reduce revenue as well as impacting hotel reputation.

__By identifying which bookings are likely to be cancelled, revenue managers and other members of the hotel’s staff can take actions to avoid potential cancellations__ such as offering services, room upgrades, discounts, entrances to shows/amusement parks, or other perks. Knowledge of cancellation behaviour is relevant not only to hotel managers’ predictions of future revenues and capacity utilisation, but to their cancellation and pricing policies, as well.

According to [Antonio, de Almeida, and Nunes (2017)]('https://ieeexplore.ieee.org/document/8260781'), guests contacted by hotels, even without being offered nothing substantial, cancel much less than guests not contacted. So, the knowledge of cancellation can help hoteliers reduce the number of people to be contacted and with that, contribute to lower cancellation rates, at controlled costs.

The data used in this project contains booking information for a city hotel and a resort hotel, and includes information such as when the booking was made, length of stay, the number of adults, children, and/or babies, and the number of available parking spaces, among other things. All personally identifying information has been removed from the data.

The data is originally from the article Hotel Booking Demand Datasets, written by [Nuno Antonio, Ana Almeida, and Luis Nunes for Data in Brief, Volume 22, February 2019](https://www.sciencedirect.com/science/article/pii/S2352340918315191). The data was downloaded and cleaned by Thomas Mock and Antoine Bichat for [#TidyTuesday during the week of February 11th, 2020](https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-02-11/readme.md).


<img src="https://www.jetsetter.com/wp-content/uploads/sites/7/2018/04/jleQRg3N-1380x690.jpeg" alt="Hotel Lobby" style="width:690px;height:345px;">


## Data Dictionary
|VARIABLE                       |TYPE      |DESCRIPTION |
|:------------------------------|:---------|:-----------|
|__hotel__                      |character | Hotel (H1 = Resort Hotel or H2 = City Hotel) |
|__is_canceled__                |double    | Value indicating if the booking was canceled (1) or not (0) |
|__lead_time__                  |double    | Number of days that elapsed between the entering date of the booking into the PMS and the arrival date |
|__arrival_date_year__          |double    | Year of arrival date|
|__arrival_date_month__         |character | Month of arrival date|
|__arrival_date_week_number__   |double    | Week number of year for arrival date|
|__arrival_date_day_of_month__  |double    | Day of arrival date|
|__stays_in_weekend_nights__   |double    | Number of weekend nights (Saturday or Sunday) the guest stayed or booked to stay at the hotel |
|__stays_in_week_nights__       |double    |  Number of week nights (Monday to Friday) the guest stayed or booked to stay at the hotel|
|__adults__                     |double    | Number of adults|
|__children__                   |double    | Number of children|
|__babies__                     |double    |Number of babies |
|__meal__                       |character | Type of meal booked. Categories are presented in standard hospitality meal packages: <br> Undefined/SC – no meal package;<br>BB – Bed & Breakfast; <br> HB – Half board (breakfast and one other meal – usually dinner); <br> FB – Full board (breakfast, lunch and dinner) |
|__country__                    |character | Country of origin. Categories are represented in the ISO 3155–3:2013 format |
|__market_segment__             |character | Market segment designation. In categories, the term “TA” means “Travel Agents” and “TO” means “Tour Operators” |
|__distribution_channel__       |character | Booking distribution channel. The term “TA” means “Travel Agents” and “TO” means “Tour Operators” |
|__is_repeated_guest__          |double    | Value indicating if the booking name was from a repeated guest (1) or not (0) |
|__previous_cancellations__     |double    | Number of previous bookings that were cancelled by the customer prior to the current booking |
|__previous_bookings_not_canceled__ |double    | Number of previous bookings not cancelled by the customer prior to the current booking |
|__reserved_room_type__         |character | Code of room type reserved. Code is presented instead of designation for anonymity reasons |
|__assigned_room_type__         |character | Code for the type of room assigned to the booking. Sometimes the assigned room type differs from the reserved room type due to hotel operation reasons (e.g. overbooking) or by customer request. Code is presented instead of designation for anonymity reasons |
|__booking_changes__            |double    | Number of changes/amendments made to the booking from the moment the booking was entered on the PMS until the moment of check-in or cancellation|
|__deposit_type__               |character | Indication on if the customer made a deposit to guarantee the booking. This variable can assume three categories:<br>No Deposit – no deposit was made;<br>Non Refund – a deposit was made in the value of the total stay cost;<br>Refundable – a deposit was made with a value under the total cost of stay. |
|__agent__                      |character | ID of the travel agency that made the booking |
|__company__                    |character | ID of the company/entity that made the booking or responsible for paying the booking. ID is presented instead of designation for anonymity reasons |
|__days_in_waiting_list__       |double    | Number of days the booking was in the waiting list before it was confirmed to the customer |
|__customer_type__              |character | Type of booking, assuming one of four categories:<br>Contract - when the booking has an allotment or other type of contract associated to it;<br>Group – when the booking is associated to a group;<br>Transient – when the booking is not part of a group or contract, and is not associated to other transient booking;<br>Transient-party – when the booking is transient, but is associated to at least other transient booking|
|__adr__                        |double    | Average Daily Rate as defined by dividing the sum of all lodging transactions by the total number of staying nights |
|__required_car_parking_spaces__|double    | Number of car parking spaces required by the customer |
|__total_of_special_requests__  |double    | Number of special requests made by the customer (e.g. twin bed or high floor)|
|__reservation_status__         |character | Reservation last status, assuming one of three categories:<br>Canceled – booking was canceled by the customer;<br>Check-Out – customer has checked in but already departed;<br>No-Show – customer did not check-in and did inform the hotel of the reason why |
|__reservation_status_date__    |double    | Date at which the last status was set. This variable can be used in conjunction with the ReservationStatus to understand when was the booking canceled or when did the customer checked-out of the hotel|



## Data Preparation
#### 1. Drop Rows with Missing Values
children, country, market_segment, distribution_channel 
#### 2. Modifying Columns
total_guests = adults + children + babies
#### 3. Remove Wrong Values
- adr feature has negative value. It does not make sense if the price is negative. 
- total_guests has the value of 0. It does not make sense if no one booked the room.
#### 4. Drop Features
Considering: percentage of null values,  information contained, high correlation with other features

## Modeling
#### 1. Preprocessing
Using Pipeline: constant imputer and binary encoder for categorical data, robust scaler for numerical data, smote

#### 2. Modeling with Default Parameters
Six models are used: Logistic Regression, DTC, RFC, Gradient Boosting Classifier, XGB Classifier, KNN. The two best models are __RFC and XGB__
![pic1](./pic_for_readme/6ModelScore.jpg)

#### 3. Modeling with Default Parameters + RFE in Pipeline
The test score using RFE is slightly drop from the non-RFE model and RFC model still has the best score<br>
![pic2](./pic_for_readme/no_rfe_vs_rfe.jpg)

#### 4. Hyperparameter Tuning RFC
The tuning is failed to make the score better. So, the default parameter RFC model pipeline will be used
![pic3](./pic_for_readme/tuning.jpg)

#### 5. Threshold Adjustment
The threshold of 0.590833 increase precision score as much as almost 4% while losing recall score 5.7%
![pic4](./pic_for_readme/threshold_adjust.jpg)

## Dashboard
#### Homepage
![pic5](./pic_for_readme/homepage.jpg)
#### Dataset Page
![pic6](./pic_for_readme/pagedataset_.JPG)
#### Visualization Page
![pic7](./pic_for_readme/pagevis_.JPG)
#### Predict and Result
![pic8](./pic_for_readme/pagepredict_.jpg)
![pic9](./pic_for_readme/pageresult_.JPG)
