/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-y4c8wsvt.us.auth0.com', // the auth0 domain prefix
    audience: 'image', // the audience set for the auth0 app
    clientId: 'SeZENWUBu7vPOQ2MaR7l3tjOddmTSq6H', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8080/login-result', // the base url of the running ionic application. 
  }
};
