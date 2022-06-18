title: Cryptopals Challenges - Set 1
date: 2022-06-12
link: crypto_pals_1

I've recently been working my way through the book "Serious Cryptography" by Jean-Philippe Aumasson. It provides
a practical discussion of many commonly used cryptographic principles, e.g. block and stream ciphers, randomness, RSA, Diffie-Helman, and TLS. 

In tandem I've been looking to improve my proficiency in the Rust programming language. A few days ago I came across 
a set of practical crypto challenges published by <a target="_blank" href="https://www.cryptopals.com/">Cryptopals</a>. 
Implementing these challenges in Rust has been a great way for me to reinforce both the cryptographic principals, and the Rust 
language constructs. 

I'm also looking to do a bit more technical writing, so I'll be summarizing my solutions to the challenges here, as well as my Rust learnings.

---------------------

The first set of challenges culminates with breaking a vigenere cipher, also known as repeating key xor. Each byte in the plain text is substituted by xor-ing with a corresponding byte in the chosen key. 

If plain text = "MY MESSAGE" 
and the key = "KEY"

Then the key is repeated to correspond to each byte in the message like so,

"MY MESSAGE"\
"KEYKEYKEYK"

Each corresponding byte is xor-ed to produce the resulting cipher text byte. One note, it's natural to think about many of these ciphers in terms of letters and words, things that we humans can read. However, almost all of these concepts operate at the byte level when actually implemented. 

The function to encrypt and decrypt repeating key xor can be implemented as follows:

```rust
pub fn operate(text: &[u8], key: &[u8]) -> Vec<u8> {
    let repeated_key: Vec<u8> = key
        .into_iter()
        .cycle()
        .take(text.len())
        .map(|v| *v)
        .collect();

    fixed_xor(text, &repeated_key)
}

fn fixed_xor(a: &[u8], b: &[u8]) -> Vec<u8> {
    assert_eq!(a.len(), b.len());

    a.iter()
        .zip(b)
        .map(|(x, y)| x ^ y)
        .collect()
}
```

One pleasant surprise for me has been how Rust can be often be written in a functional style, with a tree of expressions mapping values to other values, e.g. cycle -> take -> map. 

Back to the cipher at hand. Substitution ciphers can be vulnerable to frequency analysis. That is, the characters in a given language typically have a characteristic frequency. For example, in English R, S, T, L, N, E are the most commonly occurring letters. If we decrypt a cipher text with a given key, we'd expect the frequency of characters in the plain text output to reasonably match known frequencies of letters occuring in typical English, if the key we used to decrypt is correct. 

So our first step is to determine likely key sizes. We can then try random keys, and the one resulting in the best looking plaintext in terms of character frequency matching known English character frequency, is likely the correct key. 

I'm just going to give the function for determining the key size. There are more in depth explanations online of why the key size that minimizes the normalized hamming distance between each key size block worth of bytes is likely the key size used to encrypt. 

First, the Hamming distance function. Hamming distance is simply the count of bits that differ between to byte arrays. I had to learn a little bit about string formatting in Rust to take a byte, and convert it to a string representation of the bits in that byte. I'm using "string" loosely here. There are distinctions in Rust between `String`, `&str` (string slice), and string literals. 

```rust
pub fn hamming_distance(a: &[u8], b: &[u8]) -> u32 { 
    assert_eq!(a.len(), b.len());

    a.iter()
        .zip(b)
        .fold(0u32, |acc, (x, y)| {
            // Get a representation of the bits in each byte, x, y.
            // pad with leading zeros if necessary to fill 8 bits
            let b1 = format!("{:0>8b}", x);
            let b2 = format!("{:0>8b}", y);

            acc + b1
                .chars()
                .zip(b2.chars())
                .fold(0_u32, |sum, (c1, c2)| {
                    if c1 != c2 { sum + 1 } else { sum }
                })
        })        
}
```

Here's the function for determining key size. 

```rust
fn get_key_size(plain_text: &[u8]) -> usize {
    let mut key_hamming_distance = Vec::new();
    

    // trying key sizes from 2 to 41 bytes based on the crypto pals suggestion
    for key_size in 2..41 {
        let mut i = 0;
        let mut distance = 0.00;

        while (i + 2) * key_size < plain_text.len() {
            let word1 = &plain_text[i * key_size..(i + 1) * key_size];
            let word2 = &plain_text[(i + 1) * key_size..(i + 2) * key_size];

            distance += hamming::hamming_distance(word1, word2) as f32 / key_size as f32;

            i += 1;
        }
        
        key_hamming_distance.push((key_size, distance / (i + 1) as f32));
    }

    key_hamming_distance.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());

    key_hamming_distance[0].0
}
```

Now on to the cipher breaker. A couple Rust concepts to mention. `Option`; this was a nice way of initializing min distance, without having to do something like assign it the MAX representable `f64` value. `match` allowed me to check if `min_distance` had been assigned a value yet, and perform logic based on that. Rust also has a nice `Range` syntax. 0..=255 is a range inclusive of both 0 and 255. 0..256 would be a range from 0 to 256 *exclusive* of 256. 

To break the cipher here we simply run through all 256 possibilities for a single byte key and take the one that results in plaintext whose character frequency best matches known english character frequency. That's pretty much it for this challenge! I've left out the portion of the code where we break the cipher text into blocks, such that every byte in the block was encrypted by the same key byte. The cryptopals website describes what to do here to get the blocks. So just know that the function below is solving for a single byte of the key. 

```rust
pub fn break_cipher(cipher_bytes: &[u8]) -> u8 {
    let mut min_distance: Option<f64> = None;
    let mut key: u8 = 0;

    // 256 possibilities for a single byte key
    for c in 0..=255 {
        let plain_text: Vec<u8> = cipher_bytes
            .iter()
            .map(|cipher_letter| cipher_letter ^ c)
            .collect(); 
        
        let readable = String::from_utf8_lossy(&plain_text);

        let frequency_distance = check_frequency_match(&readable);

        min_distance = match min_distance {
            None => {
                Some(frequency_distance)
            },
            Some(current_min) => {
                if frequency_distance < current_min { 
                    key = c;
                    Some(frequency_distance)
                } else { 
                    Some(current_min)
                }
            }
        };
    };

    key
}
```
