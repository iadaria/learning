package com.iadaria.shoppinglist.db

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.iadaria.shoppinglist.entities.NoteItem
import kotlinx.coroutines.flow.Flow


@Dao
interface Dao {

    @Query("SELECT * FROM note_list")
    // automatically updating if db was edited
    fun getAllNotes(): Flow<List<NoteItem>> // without suspend

    @Query("DELETE FROM note_list WHERE id IS :id")
    suspend fun deleteNote(id: Int) // because without flow

    @Insert
    suspend fun insertNote(note: NoteItem)

    @Update
    suspend fun updateNote(note: NoteItem)
}