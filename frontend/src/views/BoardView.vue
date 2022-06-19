<template>
    <div class="header">
        <button @click="backToBoardList" class="frontpage-button">
            <img src="../arrow.jpg" class="frontpage-button-img" alt="Back">
        </button>
        <h1 > {{ this.boardName }} </h1>
        <button @click="writePost" class="frontpage-button">
            <img src="../pencil.png" class="frontpage-button-img" alt="Back">
        </button>
    </div>
    <div>
        <TablePostPage :fields='fields' :boardPostsData ="boardPostsData"> </TablePostPage>
    </div>
</template>

<script>
import TablePostPage from '../components/TablePostPage.vue'

export default {
    name: "BoardView",
    data() {
        return {
            username: '',
            boardName: '',
            fields: ['Title', '', 'Author','Like','Post Date'],
            boardPostsData: []
        }
    },
    components: {
        TablePostPage
    },
    methods: {
        async fetchThisBoardPosts() {
        const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))

        const response = await fetch('https://ptt-server-backend.azurewebsites.net/user/get_all_posts_info', {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
            body: JSON.stringify({
                "username": this.username,
                "board_name": this.boardName})
            });
            const data = await response.json()
            return data
        },
        backToBoardList() {
            this.$router.push("/Frontpage/")
        },
        writePost() {
            this.$router.push("/writepost/" + this.boardName)
        }
    },
    async created() {
        this.boardName = this.$route.params.boardName
        this.username = localStorage.getItem("sessionUsername")
        this.boardPostsData = await this.fetchThisBoardPosts()
  },
}

</script>

<style scoped>

.frontpage-button-img {
    height:50px
}

.frontpage-button {
    height: 50px;
    background: none;
    border: none
}

.header {
    display: flex;
    justify-content: space-between;
}

</style>