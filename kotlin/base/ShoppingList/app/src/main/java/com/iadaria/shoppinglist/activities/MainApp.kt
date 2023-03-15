package com.iadaria.shoppinglist.activities

import android.app.Application
import com.iadaria.shoppinglist.db.MainDatabase

class MainApp : Application() {
    val database by lazy { MainDatabase.getDataBase(this) }
}