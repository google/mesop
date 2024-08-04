# Auth

To ensure that the users of your Mesop application are authenticated, this guide provides a detailed, step-by-step process on how to integrate Firebase Authentication with Mesop using a [web component](../web-components/index.md).

Mesop is designed to be auth provider agnostic, allowing you to integrate any auth library you prefer, whether it's on the client-side (JavaScript) or server-side (Python). You can support sign-ins, including social sign-ins like Google's or any others that you prefer. The general approach involves signing in on the client-side first, then transmitting an auth token to the server-side.

## Firebase Authentication

This guide will walk you through the process of integrating Firebase Authentication with Mesop using a custom web component.

**Pre-requisites:** You will need to create a [Firebase](https://firebase.google.com/) account and project. It's free to get started with Firebase and use Firebase auth for small projects, but refer to the [pricing page](https://firebase.google.com/pricing) for the most up-to-date information.

We will be using three libraries from Firebase to build an end-to-end auth flow:

- [Firebase Web SDK](https://firebase.google.com/docs/web/learn-more): Allows you to call Firebase services from your client-side JavaScript code.
- [FirebaseUI Web](https://github.com/firebase/firebaseui-web): Provides a simple, customizable auth UI integrated with the Firebase Web SDK.
- [Firebase Admin SDK (Python)](https://firebase.google.com/docs/auth/admin/verify-id-tokens#verify_id_tokens_using_the_firebase_admin_sdk): Provides server-side libraries to integrate Firebase services, including Authentication, into your Python applications.

Let's dive into how we will use each one in our Mesop app.

### Web component

The Firebase Authentication web component is a custom component built for handling the user authentication process. It's implemented using [Lit](https://lit.dev/), a simple library for building lightweight web components.

#### JS code

```javascript title="firebase_auth_component.js"
--8<-- "mesop/examples/web_component/firebase_auth/firebase_auth_component.js"
```

**What you need to do:**

- Replace `firebaseConfig` with your Firebase project's config. Read the [Firebase docs](https://firebase.google.com/docs/web/learn-more#config-object) to learn how to get yours.
- Replace the URLs `signInSuccessUrl` with your Mesop page path and `tosUrl` and `privacyPolicyUrl` to your terms and services and privacy policy page respectively.

**How it works:**

- This creates a simple and configurable auth UI using FirebaseUI Web.
- Once the user has signed in, then a sign out button is shown.
- Whenever the user signs in or out, the web component dispatches an event to the Mesop server with the auth token, or absence of it.
- See our [web component docs](../web-components/quickstart.md#javascript-module) for more details.

#### Python code

```python title="firebase_auth_component.py"
--8<-- "mesop/examples/web_component/firebase_auth/firebase_auth_component.py"
```

**How it works:**

- Implements the Python side of the Mesop web component. See our [web component docs](../web-components/quickstart.md#python-module) for more details.

### Integrating into the app

Let's put it all together:

```python title="firebase_auth_app.py"
--8<-- "mesop/examples/web_component/firebase_auth/firebase_auth_app.py"
```

*Note* You must add `firebase-admin` to your Mesop app's `requirements.txt` file

**How it works:**

- The `firebase_auth_app.py` module integrates the Firebase Auth web component into the Mesop app. It initializes the Firebase app, defines the page where the Firebase Auth web component will be used, and sets up the state to store the user's email.
- The `on_auth_changed` function is triggered whenever the user's authentication state changes. If the user is signed in, it verifies the user's ID token and stores the user's email in the state. If the user is not signed in, it clears the email from the state.

### Next steps

Congrats! You've now built an authenticated app with Mesop from start to finish. Read the [Firebase Auth docs](https://firebase.google.com/docs/auth) to learn how to configure additional sign-in options and much more.
