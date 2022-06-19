<template>
    <div class="header">
        <button style="float:left" @click="backToIndividualBoard" class="readpost-button" >
            <img src="../arrow.jpg" class="readpost-button-img" alt="Back">
        </button>
        <h1 style="float:center; color:blue"> {{ this.postData.title }} </h1>
    </div>
    <div class="flexCenter">
        <table style="width:500px" >
            <thead>
                <tr>
                <th style="textAlign:left; color:blue; fontSize:14px"> Author </th>
                <th style="float:right; color:blue; fontSize:14px"> Like </th>
                <th style="textAlign:right; color:blue; fontSize:14px"> Post Date </th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="textAlign:left; color:blue; fontSize:25px; fontWeight:bold">  {{ this.postData.author }} </td>
                    
                    <td v-if="this.postData.likes >= this.postData.hates" 
                        style="
                        color:blue; 
                        fontSize:25px; 
                        fontWeight:bold; 
                        textAlign:right;">
                         +{{ this.postData.likes - this.postData.hates }} </td>
                    <td v-else 
                        style="
                        color:red; 
                        fontSize:20px; 
                        fontWeight:bold; 
                        textAlign:right;"> 
                        -{{ this.postData.hates - this.postData.likes }} </td>
                    
                    <td style="textAlign:right"> {{ this.postDate }} </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="container-3">
        {{ this.postData.article }}
    </div>

    <div>
        <button class="likeButton" @click="hatePost"> Hate It :( </button>
        <button class="likeButton" @click="likePost"> Like It :) </button>
    </div>
</template>

<script>
export default {
    name: "ReadPostView",
    data() { 
        return {
            username: '',
            postId: '',
            postData: [],
            postDate: ''
        }
    },
    methods: {
        async fetchPostData() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const post_id = parseInt(this.postId)

            const response = await fetch('https://ptt-server-backend.azurewebsites.net/post/read_post', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
                body: JSON.stringify({"post_id": post_id})
                });
            const data = await response.json()
            return data
        },
        async addLikes() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const post_id = parseInt(this.postId)

            const response = await fetch('https://ptt-server-backend.azurewebsites.net/post/add_likes', {
                method: 'PUT',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
                body: JSON.stringify({"post_id": post_id})
                });
            const data = await response.json()
            return data
        },
        async addHates() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const post_id = parseInt(this.postId)

            const response = await fetch('https://ptt-server-backend.azurewebsites.net/post/add_hates', {
                method: 'PUT',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
                body: JSON.stringify({"post_id": post_id})
                });
            const data = await response.json()
            return data
        },
        async likePost() {
            this.addLikes()
            window.location.reload()
        },
        async hatePost() {
            this.addHates()
            window.location.reload()
        },
        async retrieveId() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const response = await fetch('https://ptt-server-backend.azurewebsites.net/board/get_latest_post_id', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "board_name": this.boardName})
            });
            const data = await response.json()
            return data
        },
        backToIndividualBoard() {
            this.$router.push("/Board/" + this.postData.board)
        }
    },

    async created() {
        this.postId = this.$route.params.postId
        this.username = localStorage.getItem("sessionUsername")
        this.postData = await this.fetchPostData()
        this.postDate = this.postData.post_datetime.substring(0,10)
    },
}
</script>

<style scoped>

.readpost-button-img {
    height:50px
}

.readpost-button {
    height: 50px;
    background: none;
    border: none
}

.flexLeft {
    display: flex;
    justify-items: left;
    margin-bottom: 50px;
}

.flexCenter {
    display: flex;
    justify-content: center;
}

.container-3 {
  max-width: 500px;
  background: rgb(255, 255, 255);
  margin: 5px auto;
  overflow: auto;
  min-height: 350px;
  border: 1px solid steelblue;
  text-align: center;
  padding: 30px;
  border-radius: 5px;
}


.likeButton {
  display: inline-block;
  background: #333f6b;
  width: 200px;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 30px;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  font-size: 15px;
  font-family: inherit;
  margin-top: 15px;
}
</style>