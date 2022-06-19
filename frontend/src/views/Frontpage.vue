<template>
  <div id="app">
    <button class="logout-button" @click="logOut">Log Out</button>    
    <TabNav :tabs="['Favorites', 'All Boards', 'User Info']" :selected="selected" @selected="setSelected" >
      <Tab :isSelected="selected === 'Favorites'" >
          <TableBoardPage :fields='fields' :boardData="favData" v-bind:favVisible="false" @delFav="delFav"> </TableBoardPage>
      </Tab>
      <Tab :isSelected="selected === 'All Boards'" >
          <TableBoardPage :fields='fields' :boardData="boardData" v-bind:favVisible="true" @addFav="addFav" @delFav="delFav"> </TableBoardPage>
      </Tab>
      <Tab :isSelected="selected === 'User Info'" >
        <UserDetails />
      </Tab>
    </TabNav>

  </div>
</template>


<script>
import TableBoardPage from '../components/TableBoardPage.vue'
import UserDetails from '../components/UserDetails.vue'
import TabNav from '../components/TabNav.vue'
import Tab from '../components/Tab.vue'


export default {
  name: "Frontpage",
  components: {
    TableBoardPage,
    UserDetails,
    TabNav,
    Tab
  },
  data() {
    return {
      username: '',
      selected: 'Favorites',
      boardData: [],
      favData: [],
      fields: ['Board Name','     ','     ','     ','Last Post']
    }
  },
  methods: {
    setSelected(tab) {
      this.selected = tab;
    },
    async fetchAllBoardData() {
      const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))

      const response = await fetch('https://ptt-server-backend.azurewebsites.net/user/get_all_boards_info', {
          method: 'POST',
          headers: {
              'Content-type': 'application/json',
              'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
          body: JSON.stringify({"user": this.username})
        });
        const data = await response.json()
        return data
      },
    async fetchAllFavData() {
      const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))

      const response = await fetch('https://ptt-server-backend.azurewebsites.net/user/get_all_fav_info', {
          method: 'POST',
          headers: {
              'Content-type': 'application/json',
              'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
          body: JSON.stringify({"user": this.username})
        });
        const data = await response.json()
        return data
      },
    addFav(board) {
      for (let i = this.favData.length - 1; i > -1; i--) {
        if (this.favData[i].board_name == board.board_name) {
          return
        }}
      this.favData.push(board)
    },
    delFav(board_name) {
      for (let i = this.favData.length - 1; i > -1; i--) {
        if (this.favData[i].board_name == board_name) {
        this.favData.splice(i, 1);}}
    },
    logOut() {
      localStorage.clear()
      this.$router.push("/")
    }
    },
  async created() {
      this.username = localStorage.getItem("sessionUsername")
      this.boardData = await this.fetchAllBoardData()
      this.favData = await this.fetchAllFavData()
  },

}
</script>

<style>

.logout-button {
  float:right;
  border:none;
  background:none;
  color:blue;
  margin-right: 10px;
  margin-top: 5px;
  font-weight: 100;
}

.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: auto;
  text-align: center;
  background: #333f6b; /* Just to visualize the extent */ 
}
</style>
