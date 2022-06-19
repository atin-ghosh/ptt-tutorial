<template>
  <div class="input-group" style="marginTop:30px; marginBottom:10px" >
    <select name="call_type" id="call_type" v-model='searchField'>
      <option value="Title">Title</option>
      <option value="Author">Author</option>
      <option value="Likes">Likes</option>
    </select>
    <input type="search" class="form-control" v-model='search' placeholder="Search">
  </div>
  <table id="tableBoardPage" class="table">
    <thead>
      <tr>
        <!-- loop through each value of the fields to get the table header -->
        <th v-for="field in fields" :key='field' class="table-post-field"> 
          {{field}} <i class="bi bi-sort-alpha-down" aria-label='Sort Icon'></i>
        </th>
      </tr>
    </thead>
    <tbody>
        <!-- Loop through the list get the each student data -->
      <tr v-for="post in filteredPosts" :key='post'>
          <td @click="onClickGoToBoard(post.id)" role="button" class="table-posts-text"> {{ post.title }} </td>
          
          <td v-if="post.has_read">  </td>
          <td v-else> <img src="../yellow.png" alt="yellow" class="iconImg"> </td>          

          <td class="table-posts-text"> {{ post.user_name }} </td>

          <td v-if="post.likes >= post.hates" style="color:blue; fontSize:20px; fontWeight:bold;"> +{{ post.likes - post.hates }} </td>
          <td v-else style="color:red; fontSize:20px; fontWeight:bold;"> -{{ post.hates - post.likes }} </td>
          
          <td style="textAlign:left"> {{ post.post_time.substring(0,10).replace(/-/g,"/") }} </td>
      </tr>
    </tbody>
  </table> 
</template>

<script>

export default {
    username: '',
    name: 'tableBoardPage',
    props: {
      boardPostsData:{
        type: Array,
        default: ()=>[],
        }, 
      fields:{type: Array}
    },
    data() {
      return {
        search: '',
        searchField: 'Title'
      }
    },
    methods: {
      async addToReadList(post_id) {
        const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
        const response = await fetch('http://0.0.0.0:9000/user/has_read', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
        body: JSON.stringify({
            "user_name": this.username,
            "post_id": post_id})
        });   
    },
      async onClickGoToBoard(post_id) {
        this.addToReadList(post_id)
        this.$router.push("/Post/" + post_id)
      }
    },
    async created() {
        this.username = localStorage.getItem("sessionUsername")
        localStorage.setItem("sessionUsername", this.username)
  },
  computed: {
    filteredPosts() {
      var searchLike = this.search
      if (this.searchField === 'Title') {
        return this.boardPostsData.filter(post => post.title.toLowerCase().includes(this.search.toLowerCase()))
      } else if (this.searchField === 'Author') {
        return this.boardPostsData.filter(post => post.user_name.toLowerCase().includes(this.search.toLowerCase()))
      } else if (this.searchField === 'Likes') {
        return this.boardPostsData.filter(function (post) {
          let total = post.likes - post.hates
          if (searchLike >= 0) {
            return total >= searchLike;
          } else {
            return total <= searchLike;
          }
        })
      }
    },
  }
}

</script>
<style scoped>

.table-posts-text {
    text-align:left;
    color:blue;
    font-weight:150;
    font-size: 20px;
}

.table-post-field {
    text-align:left;
    color:blue;
    font-weight: 100;
    font-size: 15px;
}

.iconImg {
    height: 20px;
    width: 20px;
}

table th:hover {
        background:#f2f2f2;
      }
</style>