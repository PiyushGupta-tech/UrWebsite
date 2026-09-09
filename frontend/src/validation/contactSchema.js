import Joi from "joi";

const name = Joi.string()
  .trim()
  .min(2)
  .max(50)
  .pattern(/^[A-Za-z ]+$/)
  .required()
  .messages({
    "string.empty": "Full Name is required.",
    "string.min": "Full Name must be at least 2 characters.",
    "string.max": "Full Name must be at most 50 characters.",
    "string.pattern.base": "Full Name can contain only letters and spaces.",
    "any.required": "Full Name is required.",
  });

const email = Joi.string()
  .trim()
  .max(254)
  .email({ tlds: { allow: false } })
  .pattern(/^[^@\s]+@[^@\s]+\.[^@\s]+$/)
  .required()
  .messages({
    "string.empty": "Email Address is required.",
    "string.email": "Enter a valid email address.",
    "string.max": "Email Address must be at most 254 characters.",
    "string.pattern.base": "Email Address must contain exactly one @.",
    "any.required": "Email Address is required.",
  });

const phone = Joi.string()
  .trim()
  .pattern(/^[6-9][0-9]{9}$/)
  .required()
  .messages({
    "string.empty": "Phone Number is required.",
    "string.pattern.base": "Phone Number must be 10 digits and start with 6, 7, 8, or 9.",
    "any.required": "Phone Number is required.",
  });

const subject = Joi.string()
  .trim()
  .min(3)
  .max(120)
  .required()
  .messages({
    "string.empty": "Subject is required.",
    "string.min": "Subject must be at least 3 characters.",
    "string.max": "Subject must be at most 120 characters.",
    "any.required": "Subject is required.",
  });

const message = Joi.string()
  .trim()
  .min(10)
  .max(500)
  .required()
  .messages({
    "string.empty": "Message is required.",
    "string.min": "Message must be at least 10 characters.",
    "string.max": "Message must be 500 characters or fewer.",
    "any.required": "Message is required.",
  });

export const contactFieldSchemas = {
  name,
  email,
  phone,
  subject,
  message,
};

export const contactSchema = Joi.object(contactFieldSchemas);
