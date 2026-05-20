from django.db import transaction
from ..models import User, Pasien

class PasienService:
    @staticmethod
    @transaction.atomic
    def create_pasien(user_data, pasien_data):
        
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            full_name=user_data['full_name'],
            role='pasien'
        )
        
        pasien = Pasien.objects.create(
            user=user,
            **pasien_data
        )
        
        return pasien
    
    @staticmethod
    @transaction.atomic
    def update_pasien(pasien_id, user_data, pasien_data):
        pasien = Pasien.objects.get(id=pasien_id)
        user = pasien.user

        user.username = user_data.get('username', user.username)
        user.full_name = user_data.get('full_name', user.full_name)
        user.email = user_data.get('email', user.email)
        
        password = user_data.get('password')
        if password and password.strip():
            user.set_password(password)
        
        user.save()

        for attr, value in pasien_data.items():
            setattr(pasien, attr, value)
        
        pasien.save()
        return pasien
    
    @staticmethod
    @transaction.atomic
    def delete_pasien(pasien_id):
        pasien = Pasien.objects.get(id=pasien_id)
        
        user = pasien.user
        user.delete() 
        
        return True