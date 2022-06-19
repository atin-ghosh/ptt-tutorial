<template>
    <div class="container-2" v-if="!showEditDetails">
        <br>
        <img src="../atin_photo2.jpg" class="head-img" alt="">
        <div>
            <EditUserButton 
            @click="onClick()" 
            class="editButtonBlue" 
            backgroundColor= "#f6f8fa"
            text="Edit Profile"/>
        </div>
        <img src="../company.png" class="icon-img" alt="Company"> {{ this.userData.company }}
        <br>
        <img src="../location.png" class="icon-img" alt="Location"> {{ this.userData.location }}
        <br>
        <img src="../mail.png" class="icon-img" alt="Email"> {{ this.userData.email }}
        <br>
        <img src="../phone.png" class="icon-img" alt="Tel"> {{ this.userData.telephone }}
        <br>
    </div>
    <div v-if="showEditDetails" >
        <EditUser @edit-user="editDetails" :parentData="userData" /> 
    </div>
    <div v-if="showEditDetails">
        <EditUserButton 
        @click="onClick()" 
        class="editButtonBlack" 
        text="Close Editor"
        backgroundColor="rgb(255, 37, 37)"/>
    </div>
</template>

<script>
import EditUser from './EditUser.vue'
import EditUserButton from './EditUserButton.vue'

export default {
    name: "UserDetails",
    data() {
        return {
            username: '',
            userData: [],
            showEditDetails: false
        }
    },
    components: {
        EditUser,
        EditUserButton
    },
    emits: ['edit-user'],
    methods: {
        async editDetails(details) {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))

            const response = await fetch('http://0.0.0.0:9000/user/edit_user', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
                body: JSON.stringify({
                    "name": this.username,
                    "email": details.email,
                    "tel": details.telephone,
                    "company": details.company,
                    "location": details.location,
                    })}
            );
            this.userData.company = details.company
            this.userData.location = details.location
            this.userData.email = details.email
            this.userData.telephone = details.telephone
            this.showEditDetails = false
        },
        onClick() {
            this.showEditDetails = !this.showEditDetails
        },
        async fetchUserData() {
            const tokenInfo = JSON.parse(localStorage.getItem("sessionToken"))

            const response = await fetch('http://0.0.0.0:9000/user/get_user', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                    'Authorization': tokenInfo.token_type + " " + tokenInfo.access_token,},
                body: JSON.stringify({"user": this.username})
            });
            const data = await response.json()
            return data
        },
    },
    async created() {
        this.username = localStorage.getItem("sessionUsername")
        this.userData = await this.fetchUserData()
    },
}
</script>
    
<style>

.icon-img {
    width: 25px;
    height: 25px;
    margin-right: 20px;
}

.head-img {
  border-radius: 50%;
  margin-bottom: 30px;
  width: 250px;
  height: 250px;
}

.container-2 {
  width: 350px;
  text-align: left;
  background: rgb(255, 255, 255);
  margin: 30px auto;
  overflow: auto;
  min-height: 350px;
  border: 1px solid steelblue;
  text-align: left;
  padding-left: 50px;
  padding-right: 50px;
  padding-top: 20px;
  padding-bottom: 30px;
  border-radius: 5px;

}

.editButtonBlue {
    display: inline-block;
    background: rgb(37, 158, 61);
    color: blue;
    width:250px;
    border: none;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    border: 1px solid steelblue;
    text-decoration: none;
    font-size: 15px;

    font-family: inherit;
    margin-top: 15px;
}

.editButtonBlack {
    display: inline-block;
    color: black;
    width:250px;
    border: none;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    border: 1px solid steelblue;
    text-decoration: none;
    font-size: 15px;
    font-family: inherit;
    margin-top: 15px;
}
</style>
