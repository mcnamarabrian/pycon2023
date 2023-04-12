# Testing

Testing helps validate assumptions you make about the way your application should behave. Suffice it to say - you should test your code.

The code can be tested using the following code:

```bash
make test
```

**NOTE:** If you haven't already run `make install` you're going to get errors.

## What Is Being Tested?

The code in the [tests](./tests/) directory is set up to allow you to run unit tests. The code makes use of the events in the [events](./events/) directory to make sure you get what you expect. In this case, you're testing both the _valid_ and _invalid_ requests to our **GetBalanceFunction** and **PostPaymentFunction** to make sure the code works as expected.

## What's Next?

Now that you've [interacted with your code locally](./README-INTERACTING-LOCALLY.md) and tested it, you'll [deploy your code](./README-DEPLOYING.md) to the AWS cloud.
