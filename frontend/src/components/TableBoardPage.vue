<template>
    <div class="input-group" style="marginTop:30px; marginBottom:10px">
        <input type="search" class="form-control" v-model='search' placeholder="Search">
    </div>
    <table id="tableBoardPage" class="table">
        <thead>
            <tr>
            <!-- loop through each value of the fields to get the table header -->
            <th v-for="field in fields" :key='field' class="table-board-field"> 
                {{field}} <i class="bi bi-sort-alpha-down" aria-label='Sort Icon'></i>
            </th>
            </tr>
        </thead>
        <tbody>
            <!-- Loop through the list get the each student data -->
            <tr v-for="board in filteredBoards.sort(
                function( a, b ) {
                    a = a.board_name.toLowerCase();
                    b = b.board_name.toLowerCase();
                    return a < b ? -1 : a > b ? 1 : 0;})" :key='board'>
                <td class="table-board-text" @click="onClickGoToBoard(board.board_name)" role="button"> {{ board.board_name }} </td>
                
                <td v-if="board.has_read" style="width:10%">  </td>
                <td v-else style="width:10%"> <img src="../yellow.png" alt="yellow" class="icon-img"> </td>
        
                <td v-if="favVisible" style="width:20%"> <img src="../fav.jpg" alt="add_fav" class="icon-btn-img" @click="onClickAddFav(board)"> </td>
                <td v-else style="width:20%"> </td>

                <td> <img src="../delete.png" alt="del_fav" class="icon-btn-img" @click="onClickDelFav(board.board_name)"> </td>
                
                <td style="textAlign:left"> {{ board.last_post.substring(0,10).replace(/-/g,"/") }} </td>
            </tr>
        </tbody>
    </table>
     
</template>

<script>

import {computed,ref} from "vue";

export default {
    username: '',
    name: 'tableBoardPage',
    props:{
        boardData:{
            type: Array,
            default: ()=>[],
        },
        fields:{type: Array,},
        favVisible:{type: Boolean}
    },
    data() {
        return {
            search: '',
        }
    },
    emits: ['addFav', 'delFav'],
    methods: {
        async onClickAddFav(board) {
            var board_name = board.board_name
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const response = await fetch('https://ptt-server-backend.azurewebsites.net/board/add_fav', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "username": this.username,
                "board_name": board_name})
            });
            this.$emit('addFav', board)
        },
        async onClickDelFav(board_name) {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const response = await fetch('https://ptt-server-backend.azurewebsites.net/board/del_fav', {
            method: 'DELETE',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "username": this.username,
                "board_name": board_name})
            });
            this.$emit('delFav', board_name)
        },
        onClickGoToBoard(board_name) {
            this.$router.push("/Board/" + board_name)
        }
    },
    async created() {
        this.username = localStorage.getItem("sessionUsername")
        localStorage.setItem("sessionUsername", this.username)
  },
  computed: {
      filteredBoards() {   
        return this.boardData.filter(board => board.board_name.toLowerCase().includes(this.search.toLowerCase()))
      }
  }
}

</script>
<style scoped>

.table-board-text {
    width:50%;
    text-align:left;
    color:blue;
    font-weight:150;
    font-size: 25px;
}

.table-board-field {
    text-align:left;
    color:blue;
    font-weight: 100;
    font-size: 15px;
}

.icon-img {
    height: 20px;
    width: 20px;
}

.icon-btn-img {
    height: 20px;
    width: 20px;
    cursor: pointer;
}
table th:hover {
        background:#f2f2f2;
      }

</style>