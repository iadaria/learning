package com.iadaria.shoppinglist.db

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.iadaria.shoppinglist.entities.LibraryItem
import com.iadaria.shoppinglist.entities.NoteItem
import com.iadaria.shoppinglist.entities.ShoppingListItem
import com.iadaria.shoppinglist.entities.ShoppingListNames

@Database (entities = [LibraryItem::class, NoteItem::class, ShoppingListItem::class, ShoppingListNames::class], version = 1)
abstract class MainDatabase : RoomDatabase() {

    abstract fun getDao(): Dao

    companion object {
        @Volatile
        private var INSTANCE: MainDatabase? = null

        fun getDataBase(context: Context): MainDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    MainDatabase::class.java,
                    "shopping_list.db").build()
                instance
            }
        }
    }
}