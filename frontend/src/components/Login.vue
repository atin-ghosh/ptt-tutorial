<template>
  <div class="container-login">
    <form @submit.prevent="handleSubmit">
        <div class="form-control-2">
            <label style="marginTop:150px"> User Name </label>
            <input class="login-input" type="text" v-model="username" />
        </div>
        <div class="form-control-2">
            <label style="marginTop:5px"> Password </label>
            <input class="login-input" type="password" v-model="password" />
        </div>
        <div class="form-submit-2">
            <input type="submit" value="LOG IN" />
        </div>
    </form>
  </div>
</template>

<script>

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async handleSubmit() {

        const params = new URLSearchParams()
        params.append("username", this.username)
        params.append("password", this.password)
        try {
            const response = await fetch('http://0.0.0.0:9000/login', {
                method: 'POST',
                headers: {'Content-type': 'application/x-www-form-urlencoded'},
                body: params
            });
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json()
            localStorage.setItem("sessionToken", JSON.stringify(data))
            localStorage.setItem("sessionUsername", this.username)
            // console.log(JSON.parse(localStorage.getItem("sessionToken")))
            // console.log(localStorage.getItem("sessionUsername"))
            this.$router.push("/Frontpage")
        } catch(error){            
            this.username = ''
            this.password = ''
            console.error('Error:', error);
        }
    },
  },
}
</script>

<style scoped>

.login-input {
  background: #48537a;
}

.form-control-2 {
  margin: 5px 0;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}
.form-control-2 label {
  width: 100%;
  color: rgb(255, 255, 255);
  font-size: 15px;
  text-align: left;;
}
.form-control-2 input {
  background:#48537a; 
  width: 300px;
  height: 30px;
  margin: auto;
  padding: 3px 7px;
  font-size: 15px;
  border:0;
  border-radius: 5px;
}

.form-submit-2 {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  background:none; 
  width: 300px;
  height: 30px;
  margin-top: 75px;
  padding: 0;
  border: none;
  font-size: 15px;
  
}

.container-login {
  max-width: 400px;
  display: flex;
  justify-content: center;
  overflow: auto;
  margin: auto;
  min-height: 800px;
  text-align: center;
  padding: 5px;
  border-radius: 5px;
  width: 426px;
  padding: 56px;
  border: 8px solid white;
  margin-top: 92px;
}
</style>