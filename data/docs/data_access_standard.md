# Enterprise Data Access Standard

**Organization:** Northstar Technologies Pvt. Ltd.  
**Document Owner:** Data Governance Office  
**Version:** 2.1  
**Classification:** Internal  
**Effective Date:** 5 September 2026

> Fictional enterprise document created for semantic-search and RAG learning.

## 1. Purpose

This standard defines how employees and systems request and receive access to enterprise data.

Data access must support legitimate business use while protecting confidential and regulated information.

## 2. Data Classification

Enterprise data is classified into four categories: Public, Internal, Confidential, and Restricted.

Public information is approved for public distribution. Internal information is intended for employees and authorized contractors.

Confidential information is sensitive business information requiring restricted access. Restricted information is highly sensitive and requires additional technical and governance controls.

## 3. Access Requests

Users requesting access to enterprise data must provide a business justification, required datasets, intended use, required access level, and requested duration.

Access requests must be approved by the appropriate data owner.

## 4. Least Privilege

Users must receive only the minimum access required to perform their responsibilities.

Read-only access should be preferred when modification is not required. Administrative or bulk-export permissions require additional justification.

## 5. Sensitive Data

Access to confidential or restricted data may require data-owner approval, manager approval, privacy approval, and information-security approval.

Sensitive data must not be downloaded to unmanaged personal devices.

## 6. Non-Production Environments

Production-sensitive data should not be copied directly into development or test environments.

Where realistic test data is required, teams should use masking, tokenization, synthetic data, or anonymization.

## 7. Access Review

Access to sensitive data must be reviewed periodically.

Access should be removed when a user changes role, a project ends, a vendor engagement ends, or the business justification no longer exists.

## 8. Logging

Access to restricted datasets should be logged where technically feasible.

Audit logs should support investigation of data access, bulk downloads, permission changes, and administrative activity.
