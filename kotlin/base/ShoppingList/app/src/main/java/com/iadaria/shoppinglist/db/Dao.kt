package com.iadaria.shoppinglist.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import com.iadaria.shoppinglist.entities.NoteItem
import kotlinx.coroutines.flow.Flow


@Dao
interface Dao {

    @Query("SELECT * FROM note_list")
    // automatically updating if db was edited
    fun getAllNotes(): Flow<List<NoteItem>>

    @Insert
    suspend fun insertNote(note: NoteItem)
}