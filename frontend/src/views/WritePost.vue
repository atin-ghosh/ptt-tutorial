<template>
    <div class="container-writepost">
        <form>
            <div class="form-control-3">
                <input type="text" 
                class="formText" 
                v-model="title" 
                name="title" 
                placeholder="Title of your post" />
            </div>
            <div class="form-control-3">
                <textarea class="formText" 
                rows="20" 
                cols="50" 
                v-model="article" 
                name="article" 
                form="usrform"
                placeholder="Article">
                </textarea>
            </div>
        </form>
    </div>
    <div>
        <button class="writePostButtons" @click="writeCancel"> Cancel </button>
        <button class="writePostButtons" @click="writeAccept"> Post </button>
    </div>
</template>

<script>
export default {
    name: "WritePost",
    data() {
        return {
            username: '',
            boardName: '',
            title: '',
            article: ''
        }    
    },
    methods: {
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
        async addToReadList(post_id) {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const response = await fetch('https://ptt-server-backend.azurewebsites.net/user/has_read', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "user_name": this.username,
                "post_id": post_id})
            });   
        },
        writeCancel() {
            this.$router.push("/Board/" + this.boardName)
        },        
        async writeAccept() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))
            const response = await fetch('https://ptt-server-backend.azurewebsites.net/post/write_post', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "title": this.title,
                "article": this.article,
                "user": this.username,
                "board": this.boardName})
            });
            const new_post_id = await this.retrieveId()
            this.addToReadList(new_post_id.id)
            this.$router.push("/Board/" + this.boardName)
        }
    },
    created() {
        this.boardName = this.$route.params.boardName
        this.username = localStorage.getItem("sessionUsername")
    }
}
</script>

<style>

.add-form-2 {
    margin-left: auto;
    margin-right: auto;

}

.container-writepost {
  max-width: 700px;
  background: rgb(255, 255, 255);
  display: flex;
  justify-content: center;
  overflow: auto;
  margin: auto;
  min-height: 350px;
  border: 1px solid rgb(255, 255, 255);
  text-align: center;
  padding: 5px;
  border-radius: 5px;
}

.formText {

    width: 500px;
    margin-top: 30px;
    word-wrap: break-word;
    word-break: break-all;
    float: center;
}

.writePostButtons {
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