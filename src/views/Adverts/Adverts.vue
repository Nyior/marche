<template>
  <div class="container-fluid products">
    <Sell />

    <div
      class="row pt-5 pb-0 mt-5 mb-2 text-center d-flex justify-content-center"
    >
      <div class="col-12">
        <CategoriesList />
      </div>
    </div>

    <div class="row categories px-3 mt-0 mb-2 text-center d-flex">
      <div class="col-md-3 col-12" v-for="advert in adverts" :key="advert.id">
        <AdvertMinified :advert_object="advert" />
      </div>
    </div>

    <div
      class="row p-5  mt-5 mb-2 text-center d-flex justify-content-center"
      v-if="noAdverts && !loadingAdverts"
    >
      <div class="col-12 text-center">
        <h2 class="sub-heading mt-4 mb-2">
          no ads just yet!
        </h2>

        <router-link 
            :to="{ name: 'ads_create' }"
            class="blue-btn btn block"
                            
            >
                be the first to add an add
        </router-link>

        <router-view></router-view>
      </div>
    </div>

    <div class="row text-center d-flex justify-content-center mt-4">
      <div class="col-6">
        <p v-show="loadingAdverts">...loading...</p>
        <a v-show="next" @click="getAdverts" class>
          <strong>Load More</strong>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

import CategoriesList from "@/components/Category/CategoriesList.vue";
import AdvertMinified from "@/components/Adverts/AdvertMinified.vue";

import Sell from "@/components/Others/Sell.vue";

export default {
  name: "home",

  data() {
    return {
      adverts: [],
      next: null,
      loadingAdverts: false,
      requestUser: null,
      addedToWishList: null
    };
  },

  components: {
    CategoriesList,
    AdvertMinified,
    Sell
  },

  methods: {
    getAdverts() {
      let get_adverts_url = "api/v1/adverts/";

      if (this.next) {
        get_adverts_url = this.next.slice(22);
      }

      this.loadingAdverts = true;
      apiService(get_adverts_url, "GET").then(data => {
        this.loadingAdverts = false;
        this.adverts = [...data.results];

        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      })
      .catch(error => {
          this.loadingAdverts = false;
        });
    },

    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    }
  },

  computed: {
    noAdverts() {
      if (this.adverts.length === 0) {
        return true;
      }
    }
  },

  mounted: function() {
    this.setRequestUser();
  },
  created() {
    this.getAdverts();
    document.title = "Advertisements";
  }
};
</script>

<style></style>
