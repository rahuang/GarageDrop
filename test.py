import postmates as pm


test_key = '489913f8-8da9-431b-b2d3-05b013c87077'
test_id = 'cus_KUqEcMmgrhGHH-'


api = pm.PostmatesAPI(test_key, test_id)

pickup = pm.Location('Alice', '5520 Forbes Ave, Pittsburgh, PA', '415-555-0000')
dropoff = pm.Location('Bob', '5234 Forbes Ave, Pittsburgh, PA', '415-777-9999')

quote = pm.DeliveryQuote(api, pickup.address, dropoff.address)

print quote
# delivery = Delivery(api, 'a manifest', pickup, dropoff)
# delivery.create()

# delivery.update_status()

# delivery.cancel()