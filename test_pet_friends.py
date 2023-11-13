from api import Petfriends
from settings import valid_email, valid_password
import os

pf = Petfriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Мэт', animal_type='наглый', age='3', pet_photo='images/cat2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
       pf.add_new_pet(auth_key, "Мурзилка", "жирный", "4", "images/cat.jpg")
       _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)


        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo(name='Мэт', animal_type='наглый', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data(name=111,animal_type='наглый', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, '', '', '', '')
    assert status == 400
    assert 'error' in result

def test_get_api_key_with_invalid_password(email=valid_email, password=1212):
    status, result = pf.get_api_key(valid_email, 'invalid_password')
    assert status == 401
    assert 'error' in result

def test_get_api_key_with_invalid_credentials(email=1222, password=valid_password):
    status, result = pf.get_api_key('hjfaknvakjjbv@ndmnvs',  '12345')
    assert status == 401
    assert 'error' in result

def test_delete_pet(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    _, pets = pf.get_list_of_pets(auth_key, '')
    if len(pets['pets']) > 0:
        pet_id = pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        assert status == 200
    else:
        pytest.skip("No pets found to delete.")
