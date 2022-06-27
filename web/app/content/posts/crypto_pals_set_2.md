title: Cryptopals Challenges - Set 2
date: 2022-06-18
link: crypto_pals_2

On to Set 2 of the Cryptopals challenges! I'm only going to cover a select few of the problems presented in this set. 

In this set we move on to what the challenge authors present as "bread and butter" cryptography. Many of the challenges focus on a block cipher called AES-ECB. That's an acronym for Advanced Encryption Standard - Electronic Code Book. It turns out that this mode of AES (there are several variations) is vulnerable to a number of different attacks, that weren't even all that hard to implement. 

## Byte At A Time decryption

The first attack we'll cover is byte at a time ECB decryption. Imagine you've got an encrypted string and you'd like to know it's contents. Additionally, you have access to an AES-ECB "oracle" function. Oracle is a commonly used term in these challenges to refer to a function where you might not have access to the function internals, but you can feed the function inputs and view the outputs. So what we've got is 

> AES-128-ECB(your-string || unknown-string, random-key)

This attack exploits two key properties of AES-ECB. 

1) The same plaintext results in the same cipher text.
2) We can use property 1 to easily determine the block size of the cipher.

What is block size? AES (a block cipher) breaks a plaintext input into equal sized blocks of bytes, which are then encrypted. 

To determine the block size we can feed repeated plain text to the oracle, e.g. "AAAA", and keep increasing the length of that repeated string until we see the cipher text start to repeat itself. At that point we know we've reached the end of a block. 

In this case the block size used was 16 bytes. If we craft `your-string` to be 15 bytes long, then the first byte from the `unknown-string` will fill the last byte position in the 16 byte cipher text block. 

So now we make a lookup table. We take the 15 byte `your-string` and append all 256 possiblities for a single byte to the end of `your-string`, feed it through the oracle function to produce a corresponding cipher text, and make an entry into a hash map where the key is the corresponding cipher text and the value is `your-string + random-byte`. 

We then take the first byte from `unknown-string` and append it to `your-string`. We feed this new string into the oracle and match the output cipher text with one of the keys in the hash map. The matching entry will reveal the first byte of the cipher text. We continue this process until we've determined every byte in `unknown-string`.

A couple new Rust constructs were used in this challenge. I used a Hashmap as a lookup table. This worked similarly to Hashmaps or Dictionaries in any other language. I learned a couple ways of combining byte vectors and byte slices. I learned a new way of instantiating a vector using a macro, `vec![]`. I still need to dig into macros. I'm also appreciating how the Rust compiler helps me write safe logic. I'm getting a better feel for Rust's ownership model at this point.  

## ECB Cut and Paste

This was a fun one! In this challenge we were able to inject our own malicious data into an existing ciphertext encrypted using AES-ECB! In this challenge we model an encrypted cookie like so,

> email=foo@bar.com&uid=10&role=user

Our goal is to elevate our role to admin. We have control over the user email, so `foo@bar.com` in the example above. 

Again, the exploitable property here is that the same input to AES-ECB always results in the same output. We can use this property to determine the block size and, then craft an input email such that `role=` falls right at end of a block, causing the role, `user` to end up in the subsequent block. We can then replace that final block with one of our own making. This block might be an encrypted form of "admin" perhaps, and now we have an encrypted cookie with an elevated user role. 

## Randomness & Rust & AES-CBC, oh my
In set 2 of the challenges we were asked to implement AES-CBC mode. This mode prevents the same plaintext from always encrypting to the same ciphertext by introducing a random initial value, and chaining blocks together. 

The steps look like,

1. Create an initial value vector (IV) with size equal to the block size. 
2. XOR the IV with the first plaintext block P<sub>1</sub>.
3. XOR the resulting ciphertext block C<sub>1</sub> with the next plaintext block P<sub>2</sub> and so on. 

By creating a random IV each time we encrypt, we prevent an identical plaintext from resulting in an identical ciphertext. 

### Psuedo Random Number Generators (PRNGs)

To produce the initial value for CBC mode I had to dive into the PRNGs available in the Rust libary `Rand`. The topic of randomness is complex enough that there is a <a target="_blank" href="https://rust-random.github.io/book/">Rust Rand Book</a> covering all of the options available in the `Rand` library. 

For cryptographic purposes it's important to know that there is a difference between a run of the mill PRNG and a cryptographically secure PRNG. There is a concept of a true random number generator. A true random number generator is one in which all values are equally likely with no pattern or bias. Some natural processes can be considered true random number generators. The Rust Rand Book mentions atomic decay and thermal noise. 

Essentially, a cryptographically secure PRNG is a better approximation of a true random number generator than a non cryptographically secure PRNG. There are two key traits of a cryptographically secure PRNG outlined in the Rust Rand Book. 

 - Their state is sufficiently large that a brute-force approach simply trying all initial values is not a feasible method of finding the initial state used to produce an observed sequence of output values.

- There is no other algorithm which is sufficiently better than the brute-force method which would make it feasible to predict the next output value.


I ended up using `thread_rng` due to it's convenience. The Rust Rand Book has this to say,

```
Often you can just use thread_rng, a function which automatically initializes an RNG in thread-local memory and returns a reference to it. It is fast, good quality, and (to the best of our knowledge) cryptographically secure
```

However, there are several other cryptographically secure PRNGs within the RAND library that would likely be better choices for a production project. The Rust Rand Book actually explicitly states that `Rand` is not a cryptographic library, and recommends using specialized libraries. 

I'm not really sure where that leaves the "cryptographically secure" PRNGs in `Rand`. The documentation calls them cryptographically secure, but then recommends using something else entirely. Maybe it's a case of not wanting to take on the heavy responsiblity of making claims of `Rand` being ready for production cryptography applications. 
